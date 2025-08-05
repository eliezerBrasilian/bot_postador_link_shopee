from telegram.ext import (
    ApplicationBuilder, CommandHandler, MessageHandler, filters, CallbackQueryHandler
)
import asyncio
import os

from classes.commands_comprovantes import enviar_comprovante, receber_comprovante
from classes.commands_telegram import tratar_mensagem_texto
from classes.executores.executor_de_comandos import ExecutorDeComandos
from utils.callback_data_handler import callback_menu

class Configurador:

    def __init__(self, executor: "ExecutorDeComandos"):
        self.executor = executor

    def setup_handlers(self, app):
        app.add_handler(CommandHandler("start", self.executor.start))
        app.add_handler(CommandHandler("enviar_comprovante", enviar_comprovante))
        #waiting_comprovante = true
        app.add_handler(MessageHandler(filters.Document.ALL, receber_comprovante))
        
        app.add_handler(MessageHandler(filters.PHOTO, self.executor.receber_imagem))
        
        app.add_handler(CallbackQueryHandler(callback_menu))
        app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, tratar_mensagem_texto))
        app.add_handler(CommandHandler("auto_shopee", self.executor.auto_shopee))
       
        app.add_handler(CommandHandler("imagem", self.executor.imagem))
      
        app.add_handler(CommandHandler("gerar_post", self.executor.gerar_post))

    def iniciar(self):
        bot_token = os.getenv("BOT_TOKEN", "7619790497:AAEl_OBYi66dr1INB7lwwZwH_SWgDWW2Oe0")
        if not bot_token:
            raise ValueError("BOT_TOKEN não definido")

        app = ApplicationBuilder().token(bot_token).build()
        self.setup_handlers(app)

        loop = asyncio.get_event_loop()
        app.run_polling()
