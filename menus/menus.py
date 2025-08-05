from telegram import InlineKeyboardMarkup, InlineKeyboardButton

menu_start = InlineKeyboardMarkup([
                [
                    InlineKeyboardButton("Ir para pagamento seguro 🌠", 
                                         url="https://nubank.com.br/cobrar/u846d/6887b949-61be-41d4-b114-6f71a890022f")
                ],
                [
                    InlineKeyboardButton("Já paguei (enviar comprovante) 👌", 
                                         callback_data="enviar_comprovante")
                ]
            ])

menu_home = InlineKeyboardMarkup([
                [
                    InlineKeyboardButton("Auto Shopee", callback_data="auto_shopee")
                ],
                [
                    InlineKeyboardButton("Publicar/Gerar Posts", callback_data="gerar_post")
                ],
                [
                    InlineKeyboardButton("Add/Editar Canal do Telegram", callback_data="add_canal_grupo_telegram")
                ]
            ])

menu_apos_auto_shopee = InlineKeyboardMarkup([
                [
                    InlineKeyboardButton("Adicionar imagem do produto", callback_data="imagem")
                ],
                [
                    InlineKeyboardButton("Retornar ao menu", callback_data="start")
                ],
            ])

menu_com_apenas_um_botao_retornar_ao_menu = InlineKeyboardMarkup([
                [
                    InlineKeyboardButton("Retornar ao Menu", callback_data="start")
                ]
            ])