from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
import os

TOKEN = os.getenv("BOT_TOKEN")
DONO_ID = int(os.getenv("DONO_ID"))

async def esvaziar(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != DONO_ID:
        await update.message.reply_text("Sem permissão.")
        return

    chat = update.effective_chat

    if chat.type not in ["group", "supergroup"]:
        await update.message.reply_text("Use em um grupo.")
        return

    admins = await context.bot.get_chat_administrators(chat.id)

    for a in admins:
        if not a.user.is_bot and a.user.id != DONO_ID:
            try:
                await context.bot.ban_chat_member(chat.id, a.user.id)
            except:
                pass

    await update.message.reply_text("Grupo esvaziado com sucesso.")

app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(CommandHandler("esvaziar", esvaziar))
app.run_polling()
