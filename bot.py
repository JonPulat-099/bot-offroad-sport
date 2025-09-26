import os
import tempfile
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from main import extract_table_img2table, generate_kml

# Bot token from BotFather
BOT_TOKEN = os.getenv("BOT_TOKEN")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Send a message when the command /start is issued."""
    await update.message.reply_text(
        "Hi! Send me an image with a table and I'll convert it to a KML file for osmAnd.\n"
        "The table should have columns: Name, Latitude, Longitude, Description"
    )

async def handle_image(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle incoming images and convert to KML."""
    try:
        # Get the largest photo
        photo = update.message.photo[-1]

        # Download the image
        file = await context.bot.get_file(photo.file_id)

        # Create temporary files
        with tempfile.NamedTemporaryFile(suffix=".jpg", delete=False) as temp_image:
            await file.download_to_drive(temp_image.name)
            image_path = temp_image.name

        # Extract table from image
        df = extract_table_img2table(image_path)

        if df is not None and len(df) > 1:
            # Check if user specified columns in message
            message_text = update.message.caption or ""
            cols = [1, 2, 3, 4]  # default columns

            # Parse column selection from caption like "cols [0,1,2,3]"
            if "cols" in message_text.lower():
                try:
                    import re
                    col_match = re.search(r'cols\s*\[([0-9,\s]+)\]', message_text.lower())
                    if col_match:
                        cols = [int(x.strip()) for x in col_match.group(1).split(',')]
                except:
                    pass

            print(f"Using columns: {cols}")
            # Skip header row, use specified columns
            selected_df = df.iloc[1:, cols]

            # Generate KML file
            with tempfile.NamedTemporaryFile(suffix=".kml", delete=False) as temp_kml:
                kml_path = temp_kml.name

            generate_kml(selected_df, kml_path)

            # Send KML file back to user
            with open(kml_path, 'rb') as kml_file:
                await update.message.reply_document(
                    document=kml_file,
                    filename="points.kml",
                    caption=f"✅ Extracted {len(selected_df)} points using columns {cols}!"
                )

            # Clean up temporary files
            os.unlink(image_path)
            os.unlink(kml_path)

        else:
            await update.message.reply_text("❌ No table found in the image. Please try another image.")
            os.unlink(image_path)

    except Exception as e:
        await update.message.reply_text(f"❌ Error processing image: {str(e)}")

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Send a message when the command /help is issued."""
    help_text = """
🤖 *Table to KML Bot*

*How to use:*
1. Send me an image containing a table
2. Add caption like `cols [0,1,2,3]` to select columns
3. You'll receive a KML file for osmAnd

*Default columns: [1,2,3,4]*
*Format: Name, Latitude, Longitude, Description*

*Example captions:*
• `cols [0,1,2,3]` - use columns 0,1,2,3
• `cols [2,3,4,5]` - use columns 2,3,4,5

*Commands:*
/start - Start the bot
/help - Show this help message

Just send me an image and I'll do the rest! 📸➡️🗺️
    """
    await update.message.reply_text(help_text, parse_mode='Markdown')

def main():
    """Start the bot."""
    # Create the Application
    application = Application.builder().token(BOT_TOKEN).build()

    # Add handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(MessageHandler(filters.PHOTO, handle_image))

    # Run the bot
    print("Bot is starting...")
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == '__main__':
    main()