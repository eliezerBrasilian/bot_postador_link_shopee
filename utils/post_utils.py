import io

from outros import obtemTextoQuebrado
from moviepy.editor import *

from PIL import Image, ImageDraw, ImageFont,ImageOps

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

def gerar_imagem_estatica(imagem_bytes: bytes, nome_produto: str):
    altura_imagem = 700
    posicao_y = (altura - altura_imagem) // 2

    fundo = Image.new("RGBA", (largura, altura), (255, 255, 255, 255))

    # 1. Carrega e centraliza a imagem principal
    if imagem_bytes:
        with Image.open(io.BytesIO(imagem_bytes)) as img:
            img = img.convert("RGBA")
            img_redim = ImageOps.contain(img, (largura, altura_imagem))
            x = (largura - img_redim.width) // 2
            y = posicao_y + (altura_imagem - img_redim.height) // 2
            fundo.paste(img_redim, (x, y), img_redim)

    draw = ImageDraw.Draw(fundo)

     # 5. Retorna como bytes
    buffer = io.BytesIO()
    fundo.convert("RGB").save(buffer, format="PNG")
    buffer.seek(0)
    return buffer.getvalue()
