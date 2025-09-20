import os
import logging
import threading
import asyncio
from dotenv import load_dotenv
from telegram import Bot, Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
from fastapi import FastAPI, UploadFile, File
import uvicorn

from src.telegram_bot.rag import get_explanation
from src.utils.vector_store import ingest_docs

load_dotenv()

TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
API_HOST = os.getenv('API_HOST', '0.0.0.0')
API_PORT = int(os.getenv('API_PORT', '8080'))

if not TELEGRAM_TOKEN:
    raise ValueError('TELEGRAM_TOKEN must be set in .env or environment variables.')

bot = Bot(token=TELEGRAM_TOKEN)
app = FastAPI()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('telegram_bot')


def start(update: Update, context: CallbackContext):
    update.message.reply_text('Bot is running. Use /setchatid to register this chat. Use /ingest to upload docs.')


def set_chat_id(update: Update, context: CallbackContext):
    chat_id = str(update.effective_chat.id)
    # Persist chat id in repo-level .env
    env_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), '..', '.env')
    try:
        with open(env_path, 'a') as f:
            f.write(f'\nTELEGRAM_CHAT_ID={chat_id}\n')
    except Exception:
        with open('.env', 'a') as f:
            f.write(f'\nTELEGRAM_CHAT_ID={chat_id}\n')
    update.message.reply_text(f'Chat ID set to {chat_id}.')


def _sync_get_explanation(signal_path: str) -> str:
    """Run the async get_explanation safely from sync code."""
    try:
        return asyncio.run(get_explanation(signal_path))
    except Exception as e:
        logger.exception('LLM explanation failed')
        return f'Explanation failed: {e}'


def handle_photo_and_document(update: Update, context: CallbackContext):
    msg = update.message
    try:
        photo_file = None
        signal_path = None
        if msg.photo:
            photo_file = msg.photo[-1].get_file()
            photo_path = f'/tmp/{photo_file.file_id}.jpg'
            photo_file.download(photo_path)
        if msg.document:
            doc = msg.document.get_file()
            signal_path = f'/tmp/{doc.file_id}.json'
            doc.download(signal_path)
        if photo_file and signal_path:
            explanation = _sync_get_explanation(signal_path)
            with open(photo_path, 'rb') as ph:
                msg.reply_photo(photo=ph, caption=explanation)
        else:
            msg.reply_text('Please send a photo (screenshot) and a document (signal JSON) together.')
    except Exception as e:
        logger.exception('Error processing incoming files')
        msg.reply_text(f'Error: {e}')


def ingest_command(update: Update, context: CallbackContext):
    msg = update.message
    try:
        if msg.document:
            doc = msg.document.get_file()
            doc_path = f'/tmp/{doc.file_id}.txt'
            doc.download(doc_path)
            with open(doc_path, 'r', encoding='utf-8') as f:
                text = f.read()
            try:
                asyncio.run(ingest_docs([text]))
            except Exception:
                loop = asyncio.new_event_loop()
                threading.Thread(target=lambda: loop.run_until_complete(ingest_docs([text]))).start()
            msg.reply_text('Document ingested into vector store.')
        else:
            msg.reply_text('Please attach a document to ingest.')
    except Exception as e:
        logger.exception('Ingest failed')
        msg.reply_text(f'Ingest failed: {e}')


@app.post('/upload_trade')
async def upload_trade(signal: UploadFile = File(...), screenshot: UploadFile = File(...), chat_id: str = None):
    signal_path = f'/tmp/{signal.filename}'
    screenshot_path = f'/tmp/{screenshot.filename}'
    with open(signal_path, 'wb') as f:
        f.write(await signal.read())
    with open(screenshot_path, 'wb') as f:
        f.write(await screenshot.read())
    try:
        explanation = await get_explanation(signal_path)
    except Exception as e:
        explanation = f'Explanation failed: {e}'
    target_chat = chat_id or os.getenv('TELEGRAM_CHAT_ID')
    if not target_chat:
        return {'error': 'No chat_id configured'}
    try:
        with open(screenshot_path, 'rb') as ph:
            bot.send_photo(chat_id=target_chat, photo=ph, caption=explanation)
    except Exception as e:
        logger.exception('Failed to send photo via Telegram')
        return {'error': str(e)}
    return {'status': 'sent'}


def run_telegram_bot():
    updater = Updater(token=TELEGRAM_TOKEN, use_context=True)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler('start', start))
    dp.add_handler(CommandHandler('setchatid', set_chat_id))
    dp.add_handler(CommandHandler('ingest', ingest_command))
    dp.add_handler(MessageHandler(Filters.photo | Filters.document, handle_photo_and_document))
    updater.start_polling()
    updater.idle()


def run_api():
    uvicorn.run(app, host=API_HOST, port=API_PORT)


if __name__ == '__main__':
    t1 = threading.Thread(target=run_telegram_bot, daemon=True)
    t2 = threading.Thread(target=run_api, daemon=True)
    t1.start()
    t2.start()
    t1.join()
    t2.join()
