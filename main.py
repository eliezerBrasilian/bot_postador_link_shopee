
from telegram import BotCommand

from classes.config.configurador import Configurador
from classes.executores.executor_de_comandos import ExecutorDeComandos

async def configurar_bot(context):
  
    await context.bot.set_my_description(
        description="🤖 Eu gero posts automáticos para Telegram, Instagram e YouTube.\n"
                    "Envie imagens, links e informações de produtos que eu cuido do resto!\n\n"
                    "Bot criado por ✧˚ ༘ ⋆｡˚ @jadenstratford\n"
    )
    
    await context.bot.set_my_short_description(
        short_description="Gere posts automáticos para redes sociais"
    )
    
    
if __name__ == "__main__":
    executor = ExecutorDeComandos()

    configurador = Configurador(executor)
    configurador.iniciar()