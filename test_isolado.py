from utils.post_utils import gerar_imagem_estatica
from utils.video_utils import criar_video_a_partir_de_imagens

def ler_arquivo_como_bytes(caminho_arquivo: str) -> bytes:
    with open(caminho_arquivo, "rb") as f:
        return f.read()

# imagens_bytes = [
#     ler_arquivo_como_bytes("./assets/images/img1.jpg"),
#     ler_arquivo_como_bytes("./assets/images/img2.jpg"),
#     ler_arquivo_como_bytes("./assets/images/img3.jpg")
# ]

# criar_video_a_partir_de_imagens(
#     imagens_bytes=imagens_bytes,
#     nome_produto="MICRO-ONDAS LG EASY CLEAN 30 LITROS BRANCO",
#     output_path="teste_video_2.mp4",
#     alvo="instagram"
# )

chapeu_preto = ler_arquivo_como_bytes("./assets/images/img1.jpg")

imagem_bytes = gerar_imagem_estatica(chapeu_preto, "Tênis Nike Air Max 2024")
with open("imagem_final_post.png", "wb") as f:
    f.write(imagem_bytes)


# criar_video_estilo_story_telegram_youtube(
#     imagens_bytes=imagens_bytes,
#     nome_produto="Chapéu de esqui",
#     output_path="teste_video_2.mp4"
# )
# video_editado_bytes = video_to_story_telegram_youtube(
#     video_bytes=ler_arquivo_como_bytes("video_produto_teste.mp4"),
#     nome_produto="Camiseta Polo Masculina",
#     logo_path=logo_path,
#     audio_path=audio_path
# )

# Salvar os bytes como vídeo
# with open("video_produto_story_final.mp4", "wb") as f:
#     f.write(video_editado_bytes)



# criar_video_estilo_story_telegram_youtube(
#     imagens_bytes=imagens_bytes,
#     nome_produto="Chapéu de esqui",
#     logo_path="C:\\Users\\Eliezer\\Documents\\DEV\\PYTHON\\cospe_video\\logo.jpg",         
#     audio_path="C:\\Users\\Eliezer\\Documents\\DEV\\PYTHON\\cospe_video\\naruto.mp3",
#     output_path="video_story.mp4"
# )




# criar_video_de_imagens_locais(
#     ["imagem1.jpg"],
#     audio_path="C:\\Users\\Eliezer\\Documents\\DEV\\PYTHON\\cospe_video\\naruto.mp3"
# )

# Testa a função com imagens em bytes
# criar_video_de_bytes(
#     imagens_bytes=imagens_bytes,
#     texto="Link abaixo",
#     audio_path="C:\\Users\\Eliezer\\Documents\\DEV\\PYTHON\\cospe_video\\naruto.mp3",
#     formato="shorts",
#     output_path="video_shorts_bytes.mp4"
# )
