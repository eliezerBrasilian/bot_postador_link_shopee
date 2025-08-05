from PIL import Image, ImageDraw, ImageFont
from moviepy.editor import ImageClip

# Tamanho da imagem do texto
largura, altura = 1080, 150
imagem_texto = Image.new("RGBA", (largura, altura), (255, 255, 255, 0))  # fundo transparente

draw = ImageDraw.Draw(imagem_texto)

# Fonte (ajuste o caminho se quiser usar outra)
try:
    fonte = ImageFont.truetype("arial.ttf", 60)
except IOError:
    fonte = ImageFont.load_default()

texto = "Link abaixo"

# Usa textbbox para calcular o tamanho do texto
bbox = draw.textbbox((0, 0), texto, font=fonte)
text_largura = bbox[2] - bbox[0]
text_altura = bbox[3] - bbox[1]
x = (largura - text_largura) // 2
y = (altura - text_altura) // 2

# Desenha o texto
draw.text((x, y), texto, font=fonte, fill="black")

# Salva a imagem
imagem_texto_path = "texto_temp.png"
imagem_texto.save(imagem_texto_path)

# Cria o ImageClip
clip = ImageClip(imagem_texto_path).set_duration(15).set_position(("center", 50))

# Salva um frame de teste
clip.save_frame("teste_texto.png", t=0)
