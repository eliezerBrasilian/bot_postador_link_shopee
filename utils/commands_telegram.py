from telegram import Update
from telegram.ext import ContextTypes
from utils.resposta_utils import responder_usuario
from classes.user_state import user_state 
from outros import extrair_info_shopee
from menus.menus import menu_apos_auto_shopee

async def tratar_mensagem_texto(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    texto = update.message.text.strip()
         
    await detectar_ativacao_conta_premium(update, context, texto)

    if user_state.awaiting_nome.get(user_id):
        user_state.awaiting_nome[user_id] = False

    # Verifica se é um texto Shopee do tipo 1 (do exemplo dado)
    if "Confira" in texto and "Shopee" in texto and "Somente R$" in texto:
        await extrair_informacoes_de_texto_shopee_opcao_1(update, context, texto, user_id)

    # Verifica se é do tipo 2
    elif "Dê uma olhada em" in texto and "por R$" in texto:
        await extrair_informacoes_de_texto_shopee_opcao_2(update, context, texto, user_id)


async def extrair_informacoes_de_texto_shopee_opcao_1(update: Update, context: ContextTypes.DEFAULT_TYPE, texto: str, user_id: int):
    # exemplo simples de extração
    import re

    # Nome do produto até o primeiro "com" ou "!"
    nome_match = re.search(r"Confira (.+?) com", texto)
    nome = nome_match.group(1).strip() if nome_match else None

    # Preço promocional
    preco_match = re.search(r"Somente R\$([\d\.,]+)", texto)
    preco = preco_match.group(1).strip() if preco_match else None

    # Link (https://...)
    link_match = re.search(r"(https?://\S+)", texto)
    link = link_match.group(1).strip() if link_match else None

    if nome and link:
        user_state.produtos[user_id] = f"🔥{nome} - R$ {preco or ''}"
        user_state.links[user_id] = link
        await responder_usuario(update,
            f"✅ Produto preenchido automaticamente:\n\n<b>Nome:</b> {nome}\n<b>Preço:</b> {preco or 'Não encontrado'}\n<b>Link:</b> {link}",
            reply_markup=menu_apos_auto_shopee,
            parse_mode="HTML")
        
        return
    else:
        await responder_usuario(update, "❌ Não consegui extrair as informações corretamente.")


async def extrair_informacoes_de_texto_shopee_opcao_2(update: Update, context: ContextTypes.DEFAULT_TYPE, texto:str, user_id: int):
    nome, preco, link = extrair_info_shopee(texto)
    if nome and link:
        user_state.produtos[user_id] = f"🔥{nome} - R$ {preco}"
        user_state.links[user_id] = link
        await responder_usuario(update,
                f"✅ Produto preenchido automaticamente:\n\n<b>Nome:</b> {nome}\n<b>Preço:</b> {preco}\n<b>Link:</b> {link}",
                reply_markup=menu_apos_auto_shopee,
                parse_mode="HTML")
        return
    else:
        await responder_usuario(update, "❌ Não consegui extrair as informações corretamente.")

async def detectar_ativacao_conta_premium(update: Update, context: ContextTypes.DEFAULT_TYPE, texto:str):
 # --- NOVA VERIFICAÇÃO ---
    if "-" in texto:
        partes = texto.split("-", 2)  # no máximo 3 partes
        if len(partes) == 3 and all(p.isdigit() for p in partes):
            user_id_msg, chat_id_msg, status_msg = partes
            await responder_usuario(
                update,
                f"Formato detectado:\n<b>User ID:</b> {user_id_msg}\n<b>Chat ID:</b> {chat_id_msg}\n<b>Status:</b> {status_msg}",
                parse_mode="HTML"
            )
            
             # --- NOVO: envia mensagem para o chat do usuário (ID vindo do texto)
             
            await context.bot.send_message(
                chat_id=int(chat_id_msg),
                text="Sua conta premium vitalícia foi ativada"
                    if status_msg == "201" 
                    else "Infelizmente seu acesso Premium vitalício não foi ativado :("
            )

        return