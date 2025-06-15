from dataclasses import dataclass


@dataclass
class OauthResponseDto:
    redirect_url: str

    @classmethod
    def from_entity(cls, data: str) -> "OauthResponseDto":
        return cls(redirect_url=data)