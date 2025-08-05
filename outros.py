import re
from telegram import InlineKeyboardMarkup, InlineKeyboardButton


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
