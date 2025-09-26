# Table to KML Bot

Telegram bot that converts table images to KML files for osmAnd navigation.

## Features

- 📸 Extract tables from images using OCR
- 📝 Accept manual CSV text input
- 🗺️ Generate KML files for osmAnd
- 🔧 Custom column selection
- 🌍 Multi-language OCR support

## VPS Deployment

### Prerequisites

- VPS with Docker and Docker Compose installed
- Telegram bot token from @BotFather
- Google Cloud service account key (optional, for Google Vision API)

### Setup

1. **Clone the repository:**
```bash
git clone <your-repo-url>
cd read-image-table
```

2. **Configure environment:**
```bash
cp .env.example .env
# Edit .env and add your BOT_TOKEN
```

3. **Add Google service key (optional):**
```bash
# Place your service-key.json file in the project root
```

4. **Deploy:**
```bash
./deploy.sh
```

### Commands

```bash
# Start bot
docker-compose up -d

# View logs
docker-compose logs -f

# Stop bot
docker-compose down

# Rebuild and restart
docker-compose up -d --build
```

## Usage

### Image Input
Send an image with a table. Add caption for custom columns:
- `cols [0,1,2,3]` - use columns 0,1,2,3
- `cols [2,3,4,5]` - use columns 2,3,4,5

### Text Input
Send CSV format text:
```
Point 1,42.3601,-71.0589,Boston landmark
Point 2,40.7128,-74.0060,New York City
Point 3,34.0522,-118.2437,Los Angeles
```

Format: `Name,Latitude,Longitude,Description`

## Commands

- `/start` - Start the bot
- `/help` - Show help message