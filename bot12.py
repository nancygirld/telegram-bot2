
async def on_private_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = update.message.from_user.id
    await update.message.reply_text(f"Your user ID is {user_id}")

async def on_reply_to_bot(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if update.message.reply_to_message:
        if update.message.reply_to_message.from_user and update.message.reply_to_message.from_user.is_bot:
            user_id = update.message.from_user.id
            await update.message.reply_text(f"Your user ID is {user_id}")

def run_flask():
    # تغییر پورت به 5000 برای جلوگیری از تداخل
    app.run(host="0.0.0.0", port=5000)

async def run_bot():
    application = Application.builder().token(BOT_TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(ChatMemberHandler(new_member, ChatMemberHandler.MY_CHAT_MEMBER))
    application.add_handler(MessageHandler(filters.StatusUpdate.NEW_CHAT_MEMBERS, new_member))
    application.add_handler(MessageHandler(filters.FORWARDED, forward_info))
    application.add_handler(
        MessageHandler(filters.TEXT & (filters.ChatType.GROUP | filters.ChatType.SUPERGROUP), on_group_message)
    )
    application.add_handler(
        MessageHandler(filters.TEXT & filters.ChatType.PRIVATE, on_private_message)
    )
    application.add_handler(
        MessageHandler(filters.REPLY, on_reply_to_bot)
    )

    await application.initialize()
    await application.start()
    print("Bot started!")
    await application.updater.start_polling()
    await application.idle()

if __name__ == "__main__":
    # اجرای Flask در Thread جداگانه
    threading.Thread(target=run_flask, daemon=True).start()

    # استفاده از loop جاری و اجرای ربات
    loop = asyncio.get_event_loop()
    loop.create_task(run_bot())
    loop.run_forever()