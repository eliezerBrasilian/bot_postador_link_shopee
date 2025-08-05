import os
import io
import numpy as np

from outros import obtemTextoQuebrado
from moviepy.editor import *

from moviepy.editor import (
    AudioFileClip, ColorClip, CompositeVideoClip,
    ImageClip, VideoFileClip, concatenate_videoclips,CompositeAudioClip
)
from moviepy.audio.fx.all import audio_loop

from PIL import Image, ImageDraw, ImageFont,ImageOps
import random
from typing import Optional
import tempfile

FPS = 24
largura, altura = 1080, 1920
duracao_total: float = 20
# monkey-patch ANTIALIAS
try:
    _ = Image.ANTIALIAS  # type: ignore[reportAttributeAccessIssue]
except AttributeError:
    Image.ANTIALIAS = Image.Resampling.LANCZOS  # type: ignore[reportAttributeAccessIssue]


FONT_MONTSERRAT_SEMI_BOLD = "C:\\Users\\Eliezer\\Documents\\DEV\\PYTHON\\cospe_video\\assets\\fonts\\Montserrat-SemiBold.ttf"
FONT_MONTSERRAT_REGULAR = "C:\\Users\\Eliezer\\Documents\\DEV\\PYTHON\\cospe_video\\assets\\fonts\\Montserrat-Regular.ttf"
FONT_MONTSERRAT_BOLD = "C:\\Users\\Eliezer\\Documents\\DEV\\PYTHON\\cospe_video\\assets\\fonts\\Montserrat-Bold.ttf"
FONT_POPPINS_REGULAR = "C:\\Users\\Eliezer\\Documents\\DEV\\PYTHON\\cospe_video\\assets\\fonts\\Poppins-Regular.ttf"
# Fonte padrão
try:
    FONT_PATH = "arial.ttf"
except IOError:
    FONT_PATH = None

shopee_img = "C:\\Users\\Eliezer\\Documents\\DEV\\PYTHON\\cospe_video\\assets\\images\\shopee-icone.png"
amazon_img = "C:\\Users\\Eliezer\\Documents\\DEV\\PYTHON\\cospe_video\\assets\\images\\amazon-icone.png"
mercado_livre_img = "C:\\Users\\Eliezer\\Documents\\DEV\\PYTHON\\cospe_video\\assets\\images\\mercado-livre-icone.png"

audio_path="C:\\Users\\Eliezer\\Documents\\DEV\\PYTHON\\cospe_video\\naruto.mp3"

logo_path="C:\\Users\\Eliezer\\Documents\\DEV\\PYTHON\\cospe_video\\assets\\images\\ofertante-logo.png"

def monta_audio(video_final):
    audio = AudioFileClip(audio_path)
    if audio.duration > duracao_total:
        inicio = random.uniform(0, audio.duration - duracao_total)
        audio = audio.subclip(inicio, inicio + duracao_total)
        return video_final.set_audio(audio.volumex(0.5))
    
def monta_imagens_no_centro(imagens_bytes):
    altura_imagem = 900
    posicao_y = (altura - altura_imagem) // 2  # Centraliza verticalmente

    clips_imagens = []
    duracao_por_imagem = duracao_total / len(imagens_bytes)

    for img_bytes in imagens_bytes:
        with Image.open(io.BytesIO(img_bytes)) as img:
            img = img.convert("RGBA")
            img_redim = ImageOps.contain(img, (largura, altura_imagem))

            fundo = Image.new("RGBA", (largura, altura_imagem), (0, 0, 0, 0))
            x = (largura - img_redim.width) // 2
            y = (altura_imagem - img_redim.height) // 2
            fundo.paste(img_redim, (x, y), img_redim)

            clip = (
                ImageClip(np.array(fundo))
                .set_duration(duracao_por_imagem)
                .set_position(("center", posicao_y))
            )
            clips_imagens.append(clip)

    return clips_imagens

def gerar_text_clip(texto, largura, altura, tamanho=50, cor="black",
                    font = FONT_POPPINS_REGULAR,
                    y_offset=0, centraliza = False):
    img = Image.new("RGBA", (largura, altura), (255, 255, 255, 0))
    draw = ImageDraw.Draw(img)
    try:
        fonte = ImageFont.truetype(font, tamanho)
    except:
        fonte = ImageFont.load_default()
    bbox = draw.textbbox((0, 0), texto, font=fonte)
    x = 0  # agora alinha à esquerda
    
    if centraliza:
        x = (largura - (bbox[2] - bbox[0])) // 2     
   
    y = (altura - (bbox[3] - bbox[1])) // 2 + y_offset
    draw.text((x, y), texto, font=fonte, fill=cor)
    return ImageClip(np.array(img), transparent=True).set_duration(duracao_total)

def salvaFrame(video_final):
    # Salva um frame do segundo 0 como imagem para teste
    frame = video_final.get_frame(0)
    imagem_pil = Image.fromarray(frame)
    imagem_pil.save("preview_layout.png")

def criar_video_a_partir_de_imagens(
    imagens_bytes: list[bytes],
    nome_produto: str,
    output_path: str = "video_final.mp4",
    alvo = "instagram",
):

    # texto_botao = gerar_text_clip("Escreva: Eu quero", largura, 100, duracao_total, 60, "white").set_position(("center", altura - 140))

    # bloco_oferta = ColorClip((1080, 1080), color=(255, 0, 0), duration=duracao_total).set_position(("center", 320))
    
    subtitulo = ""
    desc = ""
    username = ""
    if alvo == "instagram":
        desc = "Peça seu link Shopee com a super oferta"
        subtitulo = "aqui no Instagram"
        username = "@ofertanteoficial"
    elif alvo == "telegram":
        subtitulo = "aqui no Telegram"
        desc = "Clique abaixo para comprar direto na Shopee"
        username = "@ofertante"
    elif alvo == "youtube":
        subtitulo = "lá no Instagram"
        desc = "Segue lá no Instagram: @ofertanteoficial"

    texto_promocoes_todo_dia = gerar_text_clip("Promoções todo dia", 1000, 100,70, "#7C3AED",
                                               font=FONT_MONTSERRAT_SEMI_BOLD).set_position((40, 20))
    texto_aqui_no_instagram = gerar_text_clip(subtitulo, 1000, 100,60, "#7C3AED").set_position((40, 90))
    
   
        
    texto_peca_seu_link = gerar_text_clip(desc, largura,
                                          90, tamanho=40, cor = "#8B0000", centraliza=True,
                                          ).set_position((0, 200))
   
    logo_clip = (ImageClip(logo_path)
                 .resize(height=200)
                 .set_position((largura - 290, 20))
                 .set_duration(duracao_total))
    
    imagens_montadas_no_centro = monta_imagens_no_centro(imagens_bytes)
    
    
    texto_username_instagram = gerar_text_clip(username, 1000, 100,tamanho=45, cor="#7C3AED",
                                               centraliza=True,
                                               font=FONT_MONTSERRAT_SEMI_BOLD).set_position((0, altura - 340))
    
    nome = obtemTextoQuebrado(nome_produto).get("primeiro_nome")
    cont = obtemTextoQuebrado(nome_produto).get("continuacao")
    texto_nome_produto = gerar_text_clip(nome, 1000, 90, tamanho= 60, cor = "#7C3AED",centraliza=True,
                                         font=FONT_MONTSERRAT_BOLD).set_position((0, altura - 260))
    
    texto_contin_nome_produto = gerar_text_clip(cont, 1000, 90, tamanho= 60, cor = "#7C3AED",centraliza=True,
                                         font=FONT_MONTSERRAT_BOLD).set_position((0, altura - 190))

    #cima
    logo1 = (ImageClip(shopee_img)
                 .resize(height=95)
                 .set_position((60, altura - 420))
                 .set_duration(duracao_total))
    #direita
    logo2 = (ImageClip(shopee_img)
                 .resize(height=95)
                 .set_position((110, altura - 370))
                 .set_duration(duracao_total))
    #esq
    logo3 = (ImageClip(shopee_img)
                 .resize(height=95)
                 .set_position((35, altura - 356))
                 .set_duration(duracao_total))

    # Define tempo de início de cada imagem
    tempo = 0
    nova_lista = []
    for clip in imagens_montadas_no_centro:
        novo = clip.set_start(tempo)
        nova_lista.append(novo)
        tempo += clip.duration
    imagens_montadas_no_centro = nova_lista

    # Agora todas as imagens sobrepõem corretamente
    video_final = CompositeVideoClip([
        ColorClip((largura, altura), color=(255, 255, 255), duration=duracao_total),
        *imagens_montadas_no_centro,
        texto_promocoes_todo_dia,
        texto_aqui_no_instagram,
        texto_peca_seu_link,
        logo_clip,
        logo1,
        logo2,
        logo3,
        texto_username_instagram,
        texto_nome_produto,
        texto_contin_nome_produto
    ], size=(largura, altura))
    
    salvaFrame(video_final)

    video_final = monta_audio(video_final)

    video_final.write_videofile(output_path, fps = FPS)
    video_final.close()
    

def criar_video_estilo_story_telegram_youtube(
    imagens_bytes: list[bytes],
    nome_produto: str,
    output_path: str = "video_final.mp4",
):

    # Clips fixos (texto, rodapé, logo etc.)
    texto_topo = gerar_text_clip("Link Abaixo", largura, 100, tamanho=70, cor="darkgreen").set_position(("center", 20))
    nome_produto_clip = gerar_text_clip(nome_produto, largura, 60, tamanho=50, cor="darkgreen").set_position(("center", 100))
    telegram_topo = gerar_text_clip("No Telegram: @ofertante", largura, 60, tamanho=45, cor="blue").set_position(("center", 180))
    
    telegram_rodape = gerar_text_clip("No Telegram: @ofertante", largura, 120, tamanho=55, cor="blue").set_position(("center", altura - 100))
   
    logo_clip = (ImageClip(logo_path)
                 .resize(height=100)
                 .set_position((largura - 120, 20))
                 .set_duration(duracao_total))
    
    imagens_montadas_no_centro = monta_imagens_no_centro(imagens_bytes)

    sequencia_imagens = concatenate_videoclips(imagens_montadas_no_centro, method="compose")

    video_final = CompositeVideoClip([
        ColorClip((largura, altura), color=(255, 255, 255), duration=duracao_total),
        sequencia_imagens,
        texto_topo,
        nome_produto_clip,
        telegram_topo,
        telegram_rodape,
        logo_clip
    ], size=(largura, altura))

    try:
        video_final = monta_audio(video_final)

        video_final.write_videofile(output_path, fps = FPS)
        video_final.close()
    except:
        print("erro ao salvar video final")
    
def video_to_story_telegram_youtube(
    video_bytes: bytes,
    nome_produto: str,
    logo_path: str,
    audio_path: Optional[str] = None,
    duracao_total: Optional[float] = None,
    FPS: int = 24,
) -> bytes:
    largura, altura = 1080, 1920

    # cria arquivos temporários
    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp4") as tmp_in:
        tmp_in.write(video_bytes)
        video_path = tmp_in.name
    tmp_out = tempfile.NamedTemporaryFile(delete=False, suffix=".mp4")
    output_path = tmp_out.name
    tmp_out.close()

    try:
        clip = VideoFileClip(video_path)

        # define duração final
        if duracao_total and clip.duration > duracao_total:
            clip = clip.subclip(0, duracao_total)
        duracao_final = duracao_total or clip.duration

        # prepara vídeo centralizado
        clip = clip.resize(width=1080).set_position(("center","center")).set_duration(duracao_final)
        fundo = ColorClip((largura,altura), color=(255,255,255), duration=duracao_final)

        # topo/rodapé e textos (idem ao criar_video_estilo_story_telegram_youtube)
        topo_bg = ColorClip((largura,220), color=(255,255,255), duration=duracao_final).set_position(("center",0))
        rodape_bg = ColorClip((largura,120), color=(255,255,255), duration=duracao_final).set_position(("center", altura-120))
        texto_topo = gerar_text_clip("Link Abaixo", largura, 100, duracao_final, tamanho=70, cor="darkgreen").set_position(("center",20))
        nome_clip  = gerar_text_clip(nome_produto, largura, 60, duracao_final, tamanho=50, cor="darkgreen").set_position(("center",100))
        telegram_topo = gerar_text_clip("No Telegram: @ofertante", largura, 60, duracao_final, tamanho=45, cor="blue").set_position(("center",180))
        telegram_rod   = gerar_text_clip("No Telegram: @ofertante", largura, 120, duracao_final, tamanho=55, cor="blue").set_position(("center", altura-100))
        logo_clip = ImageClip(logo_path).resize(height=100).set_position((largura-120,20)).set_duration(duracao_final)

        video_final = CompositeVideoClip([
            fundo, clip,
            topo_bg, rodape_bg,
            texto_topo, nome_clip,
            telegram_topo, telegram_rod,
            logo_clip
        ], size=(largura,altura)).set_duration(duracao_final)

        # --- mixagem de áudio ---
        audio_clips = []
        if clip.audio:
            orig = clip.audio.subclip(0, duracao_final).set_duration(duracao_final)
            audio_clips.append(orig)
        if audio_path and os.path.exists(audio_path):
            ext = AudioFileClip(audio_path)
            # corta ou loop
            if ext.duration < duracao_final:
                ext = ext.fx(audio_loop, duration=duracao_final)
            else:
                ext = ext.subclip(0, duracao_final)
            # reduz volume se houver áudio original
            vol = 0.3 if clip.audio else 1.0
            ext = ext.volumex(vol)
            audio_clips.append(ext)

        if audio_clips:
            mixed = CompositeAudioClip(audio_clips).set_duration(duracao_final)
            video_final = video_final.set_audio(mixed)

        # Escreve arquivo com áudio explícito
        print(f"[DEBUG] Duracao_final={duracao_final}, clip.audio={bool(clip.audio)}, audio_clips={len(audio_clips)}")
        video_final.write_videofile(
            output_path,
            fps=FPS,
            codec="libx264",
            audio=True,
            audio_codec="aac"
        )

        # retorna bytes
        with open(output_path, "rb") as f:
            return f.read()

    finally:
        clip.close()
        video_final.close()
        if os.path.exists(video_path):  os.remove(video_path)
        if os.path.exists(output_path): os.remove(output_path)
        
        
        
        
        
        
        
        
        
        
        
        
        
        
                    
def criar_clip_de_bytes(imagem_bytes: bytes, altura_destino: int, duracao: float):
    # Abre bytes como PIL Image
    imagem_pil = Image.open(io.BytesIO(imagem_bytes)).convert("RGBA")
    
    # Converte PIL para np.array
    imagem_np = np.array(imagem_pil)
    
    # Cria ImageClip e redimensiona
    clip = (ImageClip(imagem_np)
            .set_duration(duracao)
            .resize(height=altura_destino)
            .set_position("center"))
    return clip

def criar_texto_como_imagem(texto: str, largura_total: int, altura_texto: int = 150, 
                           tamanho_fonte: int = 60, cor_texto: str = "black") -> ImageClip:
    """Cria um clip de texto como imagem usando PIL."""
    imagem_texto = Image.new("RGBA", (largura_total, altura_texto), (255, 255, 255, 0))
    draw = ImageDraw.Draw(imagem_texto)

    try:
        fonte = ImageFont.truetype("arial.ttf", tamanho_fonte)
    except IOError:
        fonte = ImageFont.load_default()

    bbox = draw.textbbox((0, 0), texto, font=fonte)
    text_largura = bbox[2] - bbox[0]
    text_altura = bbox[3] - bbox[1]
    x = (largura_total - text_largura) // 2
    y = (altura_texto - text_altura) // 2
    draw.text((x, y), texto, font=fonte, fill=cor_texto)

    caminho_imagem = "texto_temp.png"
    imagem_texto.save(caminho_imagem)

    return ImageClip(caminho_imagem).set_position(("center", 50))

