from telegram import Update
from telegram.ext import ContextTypes
from classes.user_state import user_state
from utils.file_utils import salvar_arquivo
from utils.resposta_utils import responder_mensagem_acionada_via_query

async def enviar_comprovante(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    user_state.awaiting_comprovante[user_id] = True
    
    await responder_mensagem_acionada_via_query(update, context, "Envie seu comprovante agora (imagem ou PDF).")
    

async def receber_comprovante(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    
    if not user_state.awaiting_comprovante.get(user_id, False):
        return  # ignora a mensagem
   
    # processa arquivo
    if update.message.document:
        file = update.message.document
        await enviar_para_canal_privado(update,context, file)
    elif update.message.photo:
        photo = update.message.photo[-1]
        await enviar_para_canal_privado(update,context, photo)  
    else:
        await update.message.reply_text("Por favor, envie um arquivo PDF ou uma imagem.")

    # reset estado
    user_state.awaiting_comprovante[user_id] = False
    

async def enviar_para_canal_privado(update: Update, context: ContextTypes.DEFAULT_TYPE, file):
    CHAT_ID_DESTINO = -1002624250430
    caminho = await salvar_arquivo(file)
    
    await update.message.reply_text(f"Comprovante recebido, aguarde um momento para liberação de seu acesso!")
    await context.bot.send_document(
            chat_id=CHAT_ID_DESTINO,
            document=open(caminho, 'rb'),
            caption=f"Comprovante enviado pelo usuário {update.effective_user.first_name}, {update.effective_user.username}, {update.effective_user.name}\n\nId do usuario abaixo."
        )
    await context.bot.send_message(
        chat_id=CHAT_ID_DESTINO,
        text=(
            f"User ID: <code>{update.effective_user.id}-{update.effective_chat.id}-{update.effective_user.full_name}</code>\n"
        ),
        parse_mode="HTML"
    )

