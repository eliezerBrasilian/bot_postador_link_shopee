from telegram import Update
from telegram.ext import ContextTypes

from classes.commands_comprovantes import enviar_comprovante
from classes.executores.executor_de_comandos import ExecutorDeComandos

async def callback_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    executor = ExecutorDeComandos()

    if query.data == "enviar_comprovante":
        # Reaproveita o handler já existente
        await enviar_comprovante(update, context)
        
    elif query.data == "auto_shopee":
        await executor.auto_shopee(update, context)
        
    elif query.data == "start":
        await executor.start(update, context)
        
    elif query.data == "imagem":
        await executor.imagem(update, context)
        
    elif query.data == "gerar_post":
        await executor.gerar_post(update, context)
