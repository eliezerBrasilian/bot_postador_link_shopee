from telegram import Update, InputFile
from telegram.ext import ContextTypes
import time
import asyncio
from utils.resposta_utils import responder_usuario
from classes.user_state import user_state  # Importa a instância compartilhada
from outros import extrair_info_shopee, gerar_botao_com_link, mostrar_botao_gerar
from menus.menus import menu_apos_auto_shopee

start_logo = "C:\\Users\\Eliezer\\Documents\\DEV\\PYTHON\\cospe_video\\assets\\images\\start_logo.png"

async def nome(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    user_state.awaiting_nome[user_id] = True
    await responder_usuario(update, "Digite o nome do produto:")

async def link(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    user_state.awaiting_link[user_id] = True
    await responder_usuario(update, "Digite o link do produto:")

async def definir_produto(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    nome = " ".join(context.args)
    await salvar_nome_produto(update, user_id, nome)

async def linkar_produto(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    link = " ".join(context.args)
    await salvar_link_produto(update, user_id, link)

async def salvar_nome_produto(update: Update, user_id: int, nome: str):
    if not nome:
        await responder_usuario(update,"Por favor, envie o nome do produto.")
        return

    user_state.produtos[user_id] = nome
    print(update.message.chat_id)
    await responder_usuario(update,f"✅ Nome do produto definido como:\n👉 {nome}")
    await mostrar_botao_gerar(update)

async def salvar_link_produto(update: Update, user_id: int, link: str):
    if not link:
        await responder_usuario(update,"Por favor, envie o link do produto.")
        return

    user_state.links[user_id] = link
    await responder_usuario(update,f"✅ Link do produto definido com sucesso:\n👉 {link}")
    await mostrar_botao_gerar(update)

async def envia_para_canal_ofertante(update, context, caminho_saida, nome_produto, link_produto):
        timeout = 120  # segundos
        intervalo = 5  # tentar a cada 5 segundos
        inicio = time.time()
        enviado = False

        texto_formatado = (
                    "⭐🤩🪄🛒 OFERTA IMPERDÍVEL\n\n"
                    "> <b>{}</b>\n\n"
                    '<a href="{}">Pegar minha oferta🤳🏻✨🙀🥳</a>'
                ).format(nome_produto, link_produto)

        while not enviado and (time.time() - inicio < timeout):
            try:
                with open(caminho_saida, "rb") as f_canal:
                    await context.bot.send_video(
                        chat_id="@ofertante",
                        video=InputFile(f_canal),
                        caption=texto_formatado,
                        parse_mode="HTML",
                        reply_markup=gerar_botao_com_link(link_produto),
                    )
                print("✅ Enviou post para o canal")
                enviado = True
            except Exception as e:
                print(f"⚠️ Erro ao tentar enviar para o canal: {e}")
                await asyncio.sleep(intervalo)

        if not enviado:
            await responder_usuario(update,"❌ Não consegui enviar o vídeo para o canal após várias tentativas.")

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
        
    else:
        await salvar_nome_produto(update, user_id, texto)

async def extrair_informacoes_de_texto_shopee_opcao_1(update: Update, 
    context: ContextTypes.DEFAULT_TYPE, texto: str, user_id: int):
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
        user_state.produtos[user_id] = f"🔥{nome} - {preco or ''}"
        user_state.links[user_id] = link
        await responder_usuario(update,
            f"✅ Produto preenchido automaticamente:\n\n<b>Nome:</b> {nome}\n<b>Preço:</b> {preco or 'Não encontrado'}\n<b>Link:</b> {link}",
            reply_markup=menu_apos_auto_shopee,
            parse_mode="HTML")
        #mostrar_botao_gerar_video
        #await mostrar_botao_gerar(update)
        
        return
    else:
        await responder_usuario(update, "❌ Não consegui extrair as informações corretamente.")


async def extrair_informacoes_de_texto_shopee_opcao_2(update: Update, context: ContextTypes.DEFAULT_TYPE, texto:str, user_id: int):
    nome, preco, link = extrair_info_shopee(texto)
    if nome and link:
        user_state.produtos[user_id] = f"🔥{nome} - {preco}"
        user_state.links[user_id] = link
        await responder_usuario(update,
                f"✅ Produto preenchido automaticamente:\n\n<b>Nome:</b> {nome}\n<b>Preço:</b> {preco}\n<b>Link:</b> {link}",
                reply_markup=menu_apos_auto_shopee,
                parse_mode="HTML")
        await mostrar_botao_gerar(update)
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