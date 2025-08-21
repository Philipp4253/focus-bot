import os
import logging
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, MessageHandler, filters
from openai import OpenAI

# ------------------------------
# Загружаем переменные окружения
# ------------------------------
load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")

if not OPENAI_API_KEY or not TELEGRAM_TOKEN:
    raise ValueError("Ошибка: не найден TELEGRAM_TOKEN или OPENAI_API_KEY в .env")

print(f"DEBUG: TELEGRAM_TOKEN = '{TELEGRAM_TOKEN}'")
print(f"DEBUG: OPENAI_API_KEY = '{OPENAI_API_KEY[:8]}...'")  # для проверки

# ------------------------------
# Логирование
# ------------------------------
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# ------------------------------
# OpenAI клиент
# ------------------------------
client = OpenAI(api_key=OPENAI_API_KEY)

# ------------------------------
# Обработчики
# ------------------------------
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👋 Привет! Я твой Focus Coach Bot. Напиши что-нибудь, и я отвечу через GPT."
    )

async def chat(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_message = update.message.text
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": user_message}]
        )
        answer = response.choices[0].message.content
        await update.message.reply_text(answer)
    except Exception as e:
        logging.error(f"Ошибка GPT: {e}")
        await update.message.reply_text("⚠️ Ошибка при запросе к GPT, попробуй позже.")

# ------------------------------
# Запуск бота
# ------------------------------
if __name__ == "__main__":
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, chat))

    print("🤖 Focus Coach Bot запущен!")
    app.run_polling()
