from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
from gtts import gTTS
import os

TOKEN = "7587477214:AAEPzc1EhiWsbIGTu7FrS9Vv-NwiPEKhErM"
CHANNELS = ["@alishern1_youtuber", "@UzAniVoice"]
MAX_TEXTS = 4

user_text_count = {}  # foydalanuvchi matn yuborilgan soni

def start(update: Update, context: CallbackContext):
    user_id = update.effective_user.id
    user_text_count[user_id] = 0
    update.message.reply_text(
        "🎤 Salom! 4 ta matn yuboring, men ularni O‘zbekcha ovozga aylantiraman."
    )

def text_to_voice(update: Update, context: CallbackContext):
    user_id = update.effective_user.id
    chat_id = update.effective_chat.id
    text = update.message.text.strip()

    if not text:
        return

    if user_id not in user_text_count:
        user_text_count[user_id] = 0

    if user_text_count[user_id] < MAX_TEXTS:
        # gTTS bilan ovoz yaratish
        tts = gTTS(text=text, lang='uz')
        filename = f"{chat_id}_output.mp3"
        tts.save(filename)

        # Telegram ga yuborish
        with open(filename, 'rb') as audio_file:
            context.bot.send_audio(chat_id=chat_id, audio=audio_file)

        os.remove(filename)  # faylni o‘chiradi

        user_text_count[user_id] += 1
        remaining = MAX_TEXTS - user_text_count[user_id]

        if remaining > 0:
            update.message.reply_text(f"✅ {remaining} ta matn qoldi ovozlash uchun.")
        else:
            update.message.reply_text(
                "📢 Siz 4 ta matn yubordingiz! Endi quyidagi kanallarga obuna bo‘ling va /start bosing:\n" +
                "\n".join(CHANNELS)
            )
    else:
        update.message.reply_text(
            "❌ Siz 4 matndan oshdingiz. Iltimos, kanallarga obuna bo‘ling va /start bosing."
        )

def main():
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, text_to_voice))

    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()
