#!/bin/bash

set -e  # 🚨 If any command fails, stop the script

# 🧾 Configuration
REGION="eu-west-2"
REPO_NAME="greg-api"
IMAGE_TAG="latest"
PROFILE="FullAdminAccess-656074852566"  # AWS CLI profile you are using

# 🆔 Get your AWS account ID
echo "📦 Getting AWS Account ID..."
ACCOUNT_ID=$(aws sts get-caller-identity --query Account --output text --profile "$PROFILE")

# 🖼️ Construct the full image URI
IMAGE_URI="$ACCOUNT_ID.dkr.ecr.$REGION.amazonaws.com/$REPO_NAME:$IMAGE_TAG"

# 🔐 Login to ECR using AWS credentials
echo "🔐 Logging in to ECR..."
aws ecr get-login-password --region "$REGION" --profile "$PROFILE" | \
  docker login --username AWS --password-stdin "$ACCOUNT_ID.dkr.ecr.$REGION.amazonaws.com"

# 🛠️ Build your Docker image locally
echo "🐳 Building Docker image..."
docker build -t "$REPO_NAME" .

# 🏷️ Tag the image so Docker knows where to push it
echo "🏷️ Tagging image as $IMAGE_URI"
docker tag "$REPO_NAME:latest" "$IMAGE_URI"

# 🚀 Push the image to AWS ECR
echo "📤 Pushing to ECR..."
docker push "$IMAGE_URI"

# ✅ All done!
echo "✅ Done! Image pushed to: $IMAGE_URI"
