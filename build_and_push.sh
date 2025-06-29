#!/bin/bash
set -e

REGION="eu-west-2"
REPO_NAME="greg-api"
IMAGE_TAG="latest"
PROFILE="FullAdminAccess-656074852566"

echo "📦 Getting AWS Account ID..."
ACCOUNT_ID=$(aws sts get-caller-identity --query Account --output text --profile "$PROFILE")

IMAGE_URI="$ACCOUNT_ID.dkr.ecr.$REGION.amazonaws.com/$REPO_NAME:$IMAGE_TAG"

echo "🔐 Logging in to ECR..."
aws ecr get-login-password --region "$REGION" --profile "$PROFILE" | \
  docker login --username AWS --password-stdin "$ACCOUNT_ID.dkr.ecr.$REGION.amazonaws.com"

echo "🐳 Building and pushing Docker image..."
docker buildx build \
  --platform linux/amd64 \
  -t "$IMAGE_URI" \
  --push .

echo "✅ Image pushed to: $IMAGE_URI"
