import re

from classes.user_state import user_state

from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from utils.resposta_utils import responder_usuario

async def mostrar_botao_gerar(update: Update):
    user_id = update.effective_user.id
    if pode_gerar_video(user_id):
        teclado = InlineKeyboardMarkup([
            [InlineKeyboardButton("🎬 Gerar Vídeo", callback_data="gerar_video")]
        ])
        await responder_usuario(update,"Tudo pronto! Clique no botão abaixo para gerar o vídeo:", reply_markup=teclado)


def gerar_botao_com_link_e_botao_retornar_ao_menu(link_produto:str, texto:str):
    botao = InlineKeyboardMarkup([
             [
                InlineKeyboardButton(texto, url=link_produto)
             ],
             [
                InlineKeyboardButton("Retornar ao menu", callback_data="start")
             ],
    ])
    return botao

def gerar_botao_com_link(link_produto:str, texto:str):
    botao = InlineKeyboardMarkup([
             [InlineKeyboardButton(texto, url=link_produto)]
    ])
    return botao

def pode_gerar_video(user_id: int) -> bool:
    return (
        user_state.produtos.get(user_id) and
        user_state.links.get(user_id) and
        user_state.imagens.get(user_id)  # lista com pelo menos uma imagem
    )

def extrair_info_shopee(texto: str):
    nome_match = re.search(r'Dê uma olhada em (.*?) por R\$', texto)
    preco_match = re.search(r'por (R\$[\d,.]+)', texto)
    link_match = re.search(r'agora!\s*(https?://\S+)', texto)

    nome = nome_match.group(1).strip() if nome_match else ""
    preco = preco_match.group(1).strip() if preco_match else ""
    link = link_match.group(1).strip() if link_match else ""

    return nome, preco, link


def obtem_tags_a_partir_do_produto(nome_produto: str):
    tags_default = "#shopee #ofertante #ofertanteoficial #achadinhos #achadinhosshopee #achadinhoshopee"
    
    produtos_com_tags = [
        {"nome": "kit inverno", "tags": ["inverno","frio","kit"]},
        {"nome": "travesseiro antialérgico", "tags": ["travesseiro","antialérgico","travesseiroAntialérgico","saúde"]},
        {"nome": "aspirador de pó robô", "tags": ["aspirador","robô","aspiradorDePó","casa"]},
        {"nome": "cobertor manta casal", "tags": ["cobertor","manta","casal","casa","cobertorDeCasal","quarto"]},
        {"nome": "caminha para cachorro", "tags": ["cama","caminha","cachorro","dog","pet","animal","caminhaDeCachorro","camaDeCachorro","quintal"]},
        {"nome": "creatina pura monohidratada", "tags": ["creatina","academia","energético"]},
        {"nome": "Micro-Ondas LG Easy Clean 30 Litros Branco", "tags": ["microondas","lg","eletrodomésticos","eletrodomesticos","casa","cozinha"]},
        {"nome": "Carrinho de bebê Passeio Beyond 2 em 1", "tags": ["carrinho","carrinhodebebê","bebê","neném","beyond","passeio","arlivre","infantil"]},
        {"nome": "Kit Ferramentas 108 Peças Multiuso Profissional", "tags": ["kit","ferramentas","multiuso","profissional","ferramentasMultiuso","ferramentaspro","ferramentasprofissional"]},
        {"nome": "Guarda Roupa Madesa Enzo", "tags": ["guardaroupa","roupa","móveis","mobília","casa","quarto"]},
    ]
    
    def com_hifen(texto):
        return texto.replace(" ", "-")
    
    nome_produto_lower = nome_produto.lower()
    nome_produto_hifen = com_hifen(nome_produto_lower)
    tags_encontradas = []
    for item in produtos_com_tags:
        nome_item = item["nome"].lower()
        nome_item_hifen = com_hifen(nome_item)
        if (
            nome_produto_lower in nome_item
            or nome_item in nome_produto_lower
            or nome_produto_hifen in nome_item
            or nome_item in nome_produto_hifen
            or nome_produto_lower in nome_item_hifen
            or nome_item_hifen in nome_produto_lower
            or nome_produto_hifen in nome_item_hifen
            or nome_item_hifen in nome_produto_hifen
        ):
            tags_encontradas = item["tags"]
            break

    if tags_encontradas:
        tag_final = tags_default + " " + " ".join(f"#{tag}" for tag in tags_encontradas)
    else:
        tag_final = tags_default

    return tag_final

def obtem_bio(nome_produto:str, alvo = "instagram"):
    tags = obtem_tags_a_partir_do_produto(nome_produto)
    
    if alvo == "instagram":
        return f"{nome_produto.upper()}\n 🛒✨😍 Peça já seu link shopee nos comentários\n{tags}"
    
    return f"{nome_produto.upper()}\n 🛒✨😍 Segue a gente no Instagram: @ofertanteoficial"


def obtemTextoQuebrado(nome:str):

    nome_array = nome.split(" ")
    print(nome_array)

    first_string = ""
    second_string = ""
    limit_max = 20

    for palavra in nome_array:
        if first_string == "":
            first_string = palavra 
        elif len(first_string + " " + palavra) < limit_max:
            first_string =  first_string + " " + palavra
        
        else:
            if second_string == "":
                second_string = palavra 
            else:
                second_string =  second_string + " " + palavra 

    print(first_string)
    print("size: " + str(len(first_string)))
    print(second_string)
    
    return {
        "primeiro_nome": first_string,
        "continuacao": second_string
    }