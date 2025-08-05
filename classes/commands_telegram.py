from telegram import Update, InputFile
from telegram.ext import ContextTypes
import os
import tempfile
import time
import asyncio
from utils.resposta_utils import enviar_video_ao_usuario, responder_usuario
from utils.video_utils import video_to_story_telegram_youtube,criar_video_a_partir_de_imagens
from classes.user_state import user_state  # Importa a instância compartilhada
from outros import extrair_info_shopee, gerar_botao_com_link, mostrar_botao_gerar, obtem_bio
from menus.menus import menu_apos_auto_shopee
import requests
from bs4 import BeautifulSoup

start_logo = "C:\\Users\\Eliezer\\Documents\\DEV\\PYTHON\\cospe_video\\assets\\images\\start_logo.png"

async def nome(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    user_state.awaiting_nome[user_id] = True
    await responder_usuario(update, "Digite o nome do produto:")

async def link(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    user_state.awaiting_link[user_id] = True
    await responder_usuario(update, "Digite o link do produto:")

async def toggle_instagram(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    estado_atual = user_state.instagram_enabled.get(user_id, True)
    user_state.instagram_enabled[user_id] = not estado_atual
    status = "ativado" if not estado_atual else "desativado"
    await responder_usuario(update, f"📸 Geração para Instagram foi {status}.")

async def receber_video(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if user_id not in user_state.videos:
        user_state.videos[user_id] = []

    video = update.message.video  # ou .document para formatos diferentes
    file = await video.get_file()
    byte_data = await file.download_as_bytearray()
    user_state.videos[user_id].append(bytes(byte_data))
    await update.message.reply_text("✅ Vídeo recebido!")


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
                print("✅ Enviou vídeo para o canal")
                enviado = True
            except Exception as e:
                print(f"⚠️ Erro ao tentar enviar para o canal: {e}")
                await asyncio.sleep(intervalo)

        if not enviado:
            await responder_usuario(update,"❌ Não consegui enviar o vídeo para o canal após várias tentativas.")

async def handleEnvioFromImagens(update, context, user_id,imagens,nome_produto, link_produto):
    alvos = {
        #"instagram",
        "telegram",
        "youtube"    
    }
    
    for alvo in alvos:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp4") as temp_file:
                    caminho_saida = temp_file.name
                    try: 
                        criar_video_a_partir_de_imagens(
                                imagens_bytes=imagens,
                                nome_produto=nome_produto,
                                output_path=caminho_saida,
                                alvo=alvo
                            )
                        
                        await responder_usuario(update,"✅ Vídeo com formato de story gerado! Enviando agora...")

                        await responder_usuario(update,f"✅ Vídeo para {alvo} foi gerado! Enviando agora...")

                            # Enviar para o usuário
                        with open(caminho_saida, "rb") as f_usuario:
                                await enviar_video_ao_usuario(update,
                                    InputFile(f_usuario),
                                    caption=obtem_bio(nome_produto,alvo),
                                    parse_mode="HTML",
                                    reply_markup=gerar_botao_com_link(link_produto)
                                )
                                print("✅ Enviou vídeo para o usuário")
                        try:
                                os.remove(caminho_saida)
                                print(f"Arquivo temporário {caminho_saida} removido com sucesso")
                        except Exception as cleanup_error:
                                print(f"Erro ao remover arquivo temporário: {cleanup_error}")
                        
                        if alvo == "telegram":        
                            await envia_para_canal_ofertante(update, context, caminho_saida, nome_produto, link_produto)
                                
                    except Exception as main_error:
                            error_msg = f"❌ Ocorreu um erro inesperado: {str(main_error)}"
                            print(error_msg)
                            await responder_usuario(update,"❌ Ocorreu um erro durante a geração do vídeo.")
                            raise  # Re-lança a exceção se você quiser que ela seja tratada em um nível superior

async def gerar_video(update, context):
    user_id = update.effective_user.id #1738750423
    imagens      = user_state.imagens.get(user_id, [])
    videos_bytes = user_state.videos.get(user_id, [])
    nome_produto = user_state.produtos.get(user_id, "")
    link_produto = user_state.links.get(user_id, "")

    if not nome_produto:
        await responder_usuario(update,"❌ Informe o nome do produto com /produto Nome do Produto")
        return

    if not imagens and not videos_bytes:
        await responder_usuario(update,"❌ Você ainda não enviou nem imagens nem vídeos.")
        return

    await responder_usuario(update,"⏳ Gerando seus vídeos, aguarde...")

    enviados = []

    if videos_bytes:
        await responder_usuario(update,"⏳ Gerando seu vídeo editado a partir do video recebido, aguarde...")
        vb = videos_bytes[-1]  # pega o último enviado
        out_bytes = video_to_story_telegram_youtube(
            video_bytes=vb,
            nome_produto=nome_produto,
            logo_path="C:\\Users\\Eliezer\\Documents\\DEV\\PYTHON\\cospe_video\\logo.jpg",
            audio_path="C:\\Users\\Eliezer\\Documents\\DEV\\PYTHON\\cospe_video\\naruto.mp3"
        )
        # escreve em temporário e envia
        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp4") as t:
            t.write(out_bytes)
            path = t.name
        with open(path, "rb") as f:
            await enviar_video_ao_usuario(update,
                InputFile(f),
                caption="🎬 Story gerado a partir do seu vídeo original"
            )
        os.remove(path)
        enviados.append("vídeo")

    if imagens:
           await handleEnvioFromImagens(update,context, user_id,imagens,nome_produto, link_produto)
    
    # Informar ao usuário o que foi enviado
    await responder_usuario(update,
        f"✅ Terminei! Vídeos gerados a partir de: {', '.join(enviados)}."
    )

    # limpa estado
    user_state.reset_user(user_id)
    print('limpou dados do usuario')

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
    
    # AliExpress
    elif "AliExpress:" in texto and "s.click.aliexpress" in texto:
        await extrair_informacoes_de_texto_aliexpress(update, context, texto, user_id)
        
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

async def extrair_informacoes_de_texto_aliexpress(update: Update, 
    context: ContextTypes.DEFAULT_TYPE, texto: str, user_id: int):
    import re

    # Extrair preço
    preco_match = re.search(r"AliExpress:\s*R\$([\d\.,]+)", texto)
    preco = preco_match.group(1).strip() if preco_match else None

    # Extrair link
    link_match = re.search(r"(https://s\.click\.aliexpress\.com/\S+)", texto)
    link = link_match.group(1).strip() if link_match else None

    nome_produto = None
    imagem_produto = None

    if link:
        try:
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
                "Content-Language": "pt-BR"
            }
            cookies = {"intl_locale": "pt_BR"}
            page = requests.get(link, headers=headers, cookies=cookies, timeout=10)
            if page.status_code == 200:
                soup = BeautifulSoup(page.text, "html.parser")
                meta_description = soup.find("meta", property="og:title")
                meta_image = soup.find("meta", property="og:image")
                if meta_description:
                    nome_produto = meta_description.get("content")
                if meta_image:
                    imagem_produto = meta_image.get("content")
        except Exception as e:
            print(f"Erro ao buscar detalhes do produto AliExpress: {e}")

    # Se não achou nome, usa padrão
    nome_produto = nome_produto or "Produto AliExpress"

    if link:
        user_state.produtos[user_id] = f"🔥{nome_produto} - {preco or ''}"
        user_state.links[user_id] = link

        resposta = f"✅ Produto preenchido automaticamente:\n\n<b>Nome:</b> {nome_produto}\n<b>Preço:</b> {preco or 'Não encontrado'}\n<b>Link:</b> {link}"
         # Baixar imagem se existir e armazenar nos bytes
    if imagem_produto:
        try:
            img_response = requests.get(imagem_produto, timeout=10)
            if img_response.status_code == 200:
                if user_id not in user_state.imagens:
                    user_state.imagens[user_id] = []
                user_state.imagens[user_id].append(img_response.content)
        except Exception as e:
            print(f"Erro ao baixar imagem do AliExpress: {e}")

        resposta = (
            f"✅ Produto preenchido automaticamente:\n\n"
            f"<b>Nome:</b> {nome_produto}\n<b>Preço:</b> {preco or 'Não encontrado'}\n<b>Link:</b> {link}"
        )

        await responder_usuario(
            update,
            resposta,
            reply_markup=menu_apos_auto_shopee,
            parse_mode="HTML"
        )
    else:
        await responder_usuario(update, "❌ Não consegui extrair as informações corretamente do texto do AliExpress.")


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
            
    # ------------------------