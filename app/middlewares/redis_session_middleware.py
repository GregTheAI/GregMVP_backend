# requirements.txt additions
# redis==4.5.4
# aioredis==2.0.1

import asyncio
import json
import secrets
import time
from typing import Any, Dict, Optional
import redis.asyncio as redis
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response
from starlette.datastructures import MutableHeaders
import logging

logger = logging.getLogger(__name__)


class RedisSessionBackend:
    """Redis backend for session storage"""

    def __init__(self, redis_url: str, key_prefix: str = "session:", expire_time: int = 3600):
        self.redis_url = redis_url
        self.key_prefix = key_prefix
        self.expire_time = expire_time
        self.redis_client: Optional[redis.Redis] = None

    async def connect(self):
        """Initialize Redis connection"""
        try:
            self.redis_client = redis.from_url(
                self.redis_url,
                encoding="utf-8",
                decode_responses=True,
                socket_connect_timeout=5,
                socket_timeout=5,
                retry_on_timeout=True,
                health_check_interval=30
            )
            # Test connection
            await self.redis_client.ping()
            logger.info("Redis session backend connected successfully")
        except Exception as e:
            logger.error(f"Failed to connect to Redis: {e}")
            raise

    async def disconnect(self):
        """Close Redis connection"""
        if self.redis_client:
            await self.redis_client.close()

    def _get_key(self, session_id: str) -> str:
        """Generate Redis key for session"""
        return f"{self.key_prefix}{session_id}"

    async def read(self, session_id: str) -> Dict[str, Any]:
        """Read session data from Redis"""
        try:
            if not self.redis_client:
                await self.connect()

            key = self._get_key(session_id)
            data = await self.redis_client.get(key)

            if data is None:
                return {}

            session_data = json.loads(data)
            logger.debug(f"Read session {session_id}: {session_data}")
            return session_data

        except Exception as e:
            logger.error(f"Error reading session {session_id}: {e}")
            return {}

    async def write(self, session_id: str, data: Dict[str, Any]) -> bool:
        """Write session data to Redis"""
        try:
            if not self.redis_client:
                await self.connect()

            key = self._get_key(session_id)
            serialized_data = json.dumps(data, default=str)

            await self.redis_client.setex(key, self.expire_time, serialized_data)
            logger.debug(f"Wrote session {session_id}: {data}")
            return True

        except Exception as e:
            logger.error(f"Error writing session {session_id}: {e}")
            return False

    async def remove(self, session_id: str) -> bool:
        """Remove session from Redis"""
        try:
            if not self.redis_client:
                await self.connect()

            key = self._get_key(session_id)
            result = await self.redis_client.delete(key)
            logger.debug(f"Removed session {session_id}")
            return result > 0

        except Exception as e:
            logger.error(f"Error removing session {session_id}: {e}")
            return False

    async def exists(self, session_id: str) -> bool:
        """Check if session exists in Redis"""
        try:
            if not self.redis_client:
                await self.connect()

            key = self._get_key(session_id)
            result = await self.redis_client.exists(key)
            return result > 0

        except Exception as e:
            logger.error(f"Error checking session {session_id}: {e}")
            return False


class RedisSessionMiddleware(BaseHTTPMiddleware):
    """Redis-based session middleware for Starlette/FastAPI"""

    def __init__(
            self,
            app,
            redis_backend: RedisSessionBackend,
            cookie_name: str = "session",
            cookie_max_age: int = 3600,
            cookie_path: str = "/",
            cookie_domain: Optional[str] = None,
            cookie_secure: bool = True,
            cookie_httponly: bool = True,
            cookie_samesite: str = "lax"
    ):
        super().__init__(app)
        self.redis_backend = redis_backend
        self.cookie_name = cookie_name
        self.cookie_max_age = cookie_max_age
        self.cookie_path = cookie_path
        self.cookie_domain = cookie_domain
        self.cookie_secure = cookie_secure
        self.cookie_httponly = cookie_httponly
        self.cookie_samesite = cookie_samesite

    async def dispatch(self, request: Request, call_next):
        # Read session
        session_id = request.cookies.get(self.cookie_name)
        session_data = {}

        if session_id:
            session_data = await self.redis_backend.read(session_id)

        # Create session interface
        session = RedisSession(session_data, self.redis_backend, session_id)
        request.state.session = session

        # Process request
        response = await call_next(request)

        # Save session if modified
        if session.modified:
            if not session.session_id:
                session.session_id = secrets.token_urlsafe(32)

            await self.redis_backend.write(session.session_id, dict(session))

            # Set cookie
            response.set_cookie(
                key=self.cookie_name,
                value=session.session_id,
                max_age=self.cookie_max_age,
                path=self.cookie_path,
                domain=self.cookie_domain,
                secure=self.cookie_secure,
                httponly=self.cookie_httponly,
                samesite=self.cookie_samesite
            )

        return response


class RedisSession(dict):
    """Session interface that behaves like a dictionary"""

    def __init__(self, data: Dict[str, Any], backend: RedisSessionBackend, session_id: Optional[str] = None):
        super().__init__(data)
        self.backend = backend
        self.session_id = session_id
        self.modified = False

    def __setitem__(self, key: str, value: Any):
        super().__setitem__(key, value)
        self.modified = True

    def __delitem__(self, key: str):
        super().__delitem__(key)
        self.modified = True

    def pop(self, key: str, default=None):
        result = super().pop(key, default)
        if key in self:
            self.modified = True
        return result

    def clear(self):
        if self:
            super().clear()
            self.modified = True

    def update(self, *args, **kwargs):
        super().update(*args, **kwargs)
        self.modified = True

    async def regenerate_id(self):
        """Generate new session ID (useful after login)"""
        old_session_id = self.session_id
        self.session_id = secrets.token_urlsafe(32)
        self.modified = True

        # Remove old session
        if old_session_id:
            await self.backend.remove(old_session_id)


# Configuration and setup
class Settings:
    """Add these to your settings"""
    REDIS_URL: str = "redis://localhost:6379/0"  # Update for your Redis instance
    SESSION_COOKIE_NAME: str = "session"
    SESSION_EXPIRE_TIME: int = 3600  # 1 hour
    SESSION_COOKIE_SECURE: bool = True  # Set to False for local development
    SESSION_COOKIE_DOMAIN: Optional[str] = None  # or ".gregthe.ai" for subdomain sharing


# FastAPI app setup
from fastapi import FastAPI

app = FastAPI()

# Initialize Redis session backend
redis_backend = RedisSessionBackend(
    redis_url=Settings.REDIS_URL,
    expire_time=Settings.SESSION_EXPIRE_TIME
)

# Add Redis session middleware
app.add_middleware(
    RedisSessionMiddleware,
    redis_backend=redis_backend,
    cookie_name=Settings.SESSION_COOKIE_NAME,
    cookie_max_age=Settings.SESSION_EXPIRE_TIME,
    cookie_secure=Settings.SESSION_COOKIE_SECURE,
    cookie_httponly=True,
    cookie_samesite="lax",  # Critical for OAuth flows
    cookie_domain=Settings.SESSION_COOKIE_DOMAIN
)


# Startup/shutdown events
@app.on_event("startup")
async def startup_event():
    await redis_backend.connect()


@app.on_event("shutdown")
async def shutdown_event():
    await redis_backend.disconnect()


# Updated OAuth service methods
class AuthService:
    async def create_oauth_client(self, request: Request, provider: str) -> ActivityStatus:
        self.logger.info(f"received request -> {request}")
        self.logger.info(f"Session data: {dict(request.state.session)}")

        self.logger.info(f"received request to initiate {provider} OAuth login")
        try:
            redirect_url = f"{settings.BACKEND_URL}/api/v1/auth/callback/{provider}"

            oauth_state = secrets.token_urlsafe(32)
            request.state.session['oauth_state'] = oauth_state

            self.logger.info(f"OAuth state generated: {oauth_state}")
            self.logger.info(f"Session registered for {provider}: {dict(request.state.session)}")

            redirect_response = await self.oauth.google.authorize_redirect(
                request,
                redirect_uri=redirect_url,
                prompt="consent",
                state=oauth_state
            )
            url_response = redirect_response.headers["location"]
            status_code = redirect_response.status_code

            self.logger.info(f"OAuth redirect URL generated: {url_response}")

            return ActivityStatus(
                code=status_code,
                message=f"Redirect to {provider} OAuth",
                data=OauthResponseDto.from_entity(url_response)
            )
        except Exception as e:
            self.logger.error(f"Error initiating OAuth login for {provider}: {e}", exc_info=True)
            return ActivityStatus(code=500, message="Failed to create OAuth client")

    async def handle_oauth_callback(self, request: Request, provider: str) -> ActivityStatus:
        self.logger.info(f"Callback request cookies: {request.cookies}")
        self.logger.info(f"Callback session data: {dict(request.state.session)}")
        self.logger.info(f"Callback query params: {dict(request.query_params)}")

        try:
            # Verify state parameter
            received_state = request.query_params.get('state')
            stored_state = request.state.session.get('oauth_state')

            if not received_state or not stored_state or received_state != stored_state:
                self.logger.error(f"Invalid state parameter. Received: {received_state}, Stored: {stored_state}")
                return ActivityStatus(code=400, message="Invalid state parameter - possible CSRF attack")

            # Clear the state from session
            request.state.session.pop('oauth_state', None)

            # Continue with OAuth token exchange...
            # ... rest of your OAuth callback logic

        except Exception as e:
            self.logger.error(f"Error in OAuth callback: {e}", exc_info=True)
            return ActivityStatus(code=500, message="OAuth callback failed")


# Docker Compose Redis service (add to your docker-compose.yml)
"""
services:
  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"
    volumes:
      - redis_data:/data
    command: redis-server --appendonly yes
    restart: unless-stopped

  your-api:
    # ... your existing API service config
    depends_on:
      - redis
    environment:
      - REDIS_URL=redis://redis:6379/0

volumes:
  redis_data:
"""