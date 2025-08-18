import os
import tempfile

from telegram import InputFile, Update
from telegram.ext import ContextTypes

from api.BotCuspidorApi import BotCuspidorAPI
from api.CacheServiceApi import CacheServiceApi
from classes.commands_comprovantes import receber_comprovante
from outros import gerar_botao_com_link
from utils.resposta_utils import enviar_foto_ao_usuario, responder_usuario

from classes.user_state import user_state 
from menus.menus import menu_com_apenas_um_botao_retornar_ao_menu, menu_start,menu_home

#aqui estou dentro de /app
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

start_logo = os.path.join(BASE_DIR, "assets", "images", "start_logo.png")

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
            canais = await self.api.listar_canais(user_id)
        
            user_state.canais[user_id] = canais
        
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
        api = CacheServiceApi()
        
        dto = await api.retrieveDataByUserId(user_id)
        if dto != None:
            dto.awaitingTituloProduto = 1
            await api.updateData(dto)
            await responder_usuario(update, "Cole a descrição da Shopee")
        
        
    async def add_canal_telegram(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        user_id = update.effective_user.id
        api = CacheServiceApi()
        
        dto = await api.retrieveDataByUserId(user_id)
        if dto != None:
            dto.awaitingCanalTelegram = 1
            await api.updateData(dto)
            await responder_usuario(update, "Adicione seu grupo ou canal aqui por exemplo: @teste")   


    async def imagem(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        await responder_usuario(update, "Envie a imagem que você deseja usar em seu post.")
        
    async def receber_imagem(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        user_id = update.effective_user.id
        
        photo = update.message.photo[-1]
        file = await photo.get_file()
        byte_data = await file.download_as_bytearray()

        user_state.imagem[user_id] = bytes(byte_data)
        
        api = CacheServiceApi()
        
        dto = await api.retrieveDataByUserId(user_id)
        if dto != None:
            if dto.awaitingComprovante == 1:
                await responder_usuario(update, "✅ Comprovante recebido, aguarde um momento para liberação do seu acesso vitalício premium!")
                
                #processar comprovante
                await receber_comprovante(update,context)
                return
            
            await responder_usuario(update, "✅ Imagem recebida!",       reply_markup=menu_com_apenas_um_botao_retornar_ao_menu)

    async def gerar_post(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        user_id = update.effective_user.id
        
        api = CacheServiceApi()
        data = await api.retrieveDataByUserId(user_id)
        if data != None:
           
            nome_produto = data.tituloProduto
            link_produto = data.linkProduto
            imagem = user_state.imagem.get(user_id, b"")

            if not nome_produto or not link_produto:
                await responder_usuario(update, "❌ Antes de gerar o post, envie o nome e o link do produto.")
                return

            if len(imagem) == 0:
                await responder_usuario(update, "❌ Para gerar o post, você precisa escolher uma imagem.")
                return

            legenda = (
                f"<b>{nome_produto}</b>\n\n"
                f"<a href=\"{link_produto}\">Pegar minha oferta 😊❤️😄👌</a>"
            )

            with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as temp_img:
                temp_img.write(imagem)
                temp_img_path = temp_img.name
        
            await enviar_post_para_canal_telegram(update, context.bot, temp_img_path, legenda, link_produto, user_id)
       
            try:
                os.remove(temp_img_path)
            except Exception as e:
                print(f"Erro ao deletar imagem temporária: {e}")

async def enviar_post_para_canal_telegram(update, bot, caminho_imagem,legenda, link_produto, user_id:int):
    canais = user_state.get_canais(user_id)
    
    for canal in canais:
        username = canal.get("username")
        try:
            with open(caminho_imagem, "rb") as img_file:
                await bot.send_photo(
                    chat_id=username,
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
            await responder_usuario(
                    update,
                    f"❌ Erro ao enviar post para o canal/grupo: {e}",
                    reply_markup=menu_com_apenas_um_botao_retornar_ao_menu
                )
            
