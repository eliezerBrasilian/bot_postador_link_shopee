import os
import tempfile

from telegram import InputFile, Update
from telegram.ext import ContextTypes

from api.BotCuspidorApi import BotCuspidorAPI
from outros import gerar_botao_com_link
from utils.resposta_utils import enviar_foto_ao_usuario, responder_usuario
from menus.menus import menu_start,menu_home

from classes.user_state import user_state 
from menus.menus import menu_com_apenas_um_botao_retornar_ao_menu

start_logo = "C:\\Users\\Eliezer\\Documents\\DEV\\PYTHON\\cospe_video\\assets\\images\\start_logo.png"

class ExecutorDeComandos:

    def __init__(self):
        self.api = BotCuspidorAPI()
            
    async def start(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        user_id = update.effective_user.id
        
        premium = await self.api.is_premium(user_id)
        
        if not premium:
            await context.bot.set_my_commands([
        ("start", "Iniciar a conversa com o bot"),
        ("enviar_comprovante", "Enviar comprovante de pagamento")
    ])
            chave_pix = (
                "00020126580014BR.GOV.BCB.PIX01363ff83fd1-8c99-40e0-b934-"
                "051891f6005152040000530398654041.005802BR5925Eliezer Assuncao "
                "de Paulo6009SAO PAULO62140510X4fRQw6Vr4630401DC"
            )
            legenda = (
                "🤩📲 Vem gerar posts no automático para Telegram, Instagram e Youtube\n"
                "‧˚₊•┈┈┈┈୨୧┈┈┈┈•‧₊˚⊹ Chave Pix ‧˚₊•┈┈┈┈୨୧┈┈┈┈•‧₊˚⊹\n\n"
                f"<code>{chave_pix}</code>\n\n"
                "Selecione e copie a chave acima ou clique no botão abaixo:"
            )
 
            with open(start_logo, "rb") as img_file:
                await enviar_foto_ao_usuario(
                    update,
                    foto=InputFile(img_file),
                    caption=legenda,
                    reply_markup=menu_start,
                    parse_mode="HTML"
                )
        else:
            await context.bot.set_my_commands([
                ("start", "Iniciar a conversa com o bot")
            ])
            #user_state.reset_user(user_id)
            await responder_usuario(
                update,
                f"Oi {update.effective_user.first_name}!\nUse o menu abaixo",
                reply_markup=menu_home
            )
            
    async def auto_shopee(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        user_id = update.effective_user.id
        user_state.awaiting_nome[user_id] = True
        await responder_usuario(update, "Cole a informação da Shopee que contém nome, preço e link:")
        
    async def add_canal_telegram(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        user_id = update.effective_user.id
        user_state.awaiting_nome[user_id] = True
        await responder_usuario(update, "Adicione seu grupo ou canal aqui por exemplo: @teste")   

    async def imagem(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        await responder_usuario(update, "Envie a imagem que você deseja usar em seu post.")
        
    async def receber_imagem(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        user_id = update.effective_user.id
        if user_id not in user_state.imagens:
            user_state.imagens[user_id] = []

        photo = update.message.photo[-1]
        file = await photo.get_file()
        byte_data = await file.download_as_bytearray()

        user_state.imagens[user_id].append(bytes(byte_data))
        await responder_usuario(update, "✅ Imagem recebida!",       reply_markup=menu_com_apenas_um_botao_retornar_ao_menu)

    async def gerar_post(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        user_id = update.effective_user.id
        nome_produto = user_state.produtos.get(user_id, "")
        link_produto = user_state.links.get(user_id, "")
        imagens = user_state.imagens.get(user_id, [])

        if not nome_produto or not link_produto:
            await responder_usuario(update, "❌ Antes de gerar o post, envie o nome e o link do produto.")
            return

        if not imagens:
            await responder_usuario(update, "❌ Para gerar o post, você precisa enviar pelo menos uma imagem.")
            return

        legenda = (
            f"<b>{nome_produto}</b>\n\n"
            f"<a href=\"{link_produto}\">Pegar minha oferta 😊❤️😄👌</a>"
        )

        ultima_imagem = imagens[-1]

        with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as temp_img:
            temp_img.write(ultima_imagem)
            temp_img_path = temp_img.name
        
        await enviar_post_para_canal_telegram(update, context.bot, temp_img_path, legenda, link_produto)
       
        try:
            os.remove(temp_img_path)
        except Exception as e:
            print(f"Erro ao deletar imagem temporária: {e}")

async def enviar_post_para_canal_telegram(update, bot, caminho_imagem,legenda, link_produto):
    try:
        with open(caminho_imagem, "rb") as img_file:
            await bot.send_photo(
                chat_id="@ofertante",
                photo=InputFile(img_file),
                caption=legenda,
                parse_mode="HTML",
                reply_markup=gerar_botao_com_link(link_produto, "Pegar minha oferta🤳🏻✨🙀🥳")
            )
        await responder_usuario(
                update,
                f"✅ Post enviado com sucesso para o canal/grupo.",
                reply_markup=menu_com_apenas_um_botao_retornar_ao_menu
            )
    except Exception as e:
        print(f"❌ Erro ao enviar post para o canal/grupo: {e}")
