#!/bin/bash

# VPS Deployment Script for Table to KML Bot

echo "🚀 Deploying Table to KML Bot..."

# Check if .env file exists
if [ ! -f .env ]; then
    echo "❌ .env file not found!"
    echo "📝 Copy .env.example to .env and fill in your BOT_TOKEN"
    exit 1
fi

# Check if service-key.json exists
if [ ! -f service-key.json ]; then
    echo "❌ service-key.json not found!"
    echo "📝 Add your Google Cloud service account key as service-key.json"
    exit 1
fi

# Stop existing container if running
echo "🛑 Stopping existing container..."
docker-compose down

# Build and start the bot
echo "🔨 Building Docker image..."
docker-compose build

echo "▶️ Starting bot..."
docker-compose up -d

echo "✅ Bot deployed successfully!"
echo "📊 Check status: docker-compose logs -f"
echo "🛑 Stop bot: docker-compose down"