import os
from telegram import Update
from telegram.ext import Application, MessageHandler, filters
import groq

# Replace with your credentials
TELEGRAM_BOT_TOKEN = "your-telegram-bot-token"
GROQ_API_KEY = "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"
GROUP_CHAT_ID = -1001234567890  # Replace with your actual group chat ID

client = groq.Client(api_key=GROQ_API_KEY)

# Function to correct grammar using Groq API
async def correct_grammar(text):
    response = client.chat.completions.create(
        model="llama3-8b-8192",
        messages=[{"role": "user", "content": f"Correct this sentence: {text}"}]
    )
    return response.choices[0].message.content.strip()

# Function to handle messages
async def handle_message(update: Update, context):
    chat_id = update.message.chat_id  # Get chat ID
    if chat_id == GROUP_CHAT_ID:  # Ensure it's from the correct group
        user_text = update.message.text
        corrected_text = await correct_grammar(user_text)
        await update.message.reply_text(corrected_text)

# Start the bot
def main():
    app = Application.builder().token(TELEGRAM_BOT_TOKEN).build()
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.run_polling()

if __name__ == "__main__":
    main()
