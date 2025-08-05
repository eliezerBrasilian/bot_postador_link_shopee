from dotenv import load_dotenv
import os

# Carrega variáveis do arquivo .env
load_dotenv()
token = os.getenv('BOT_TOKEN')
print(token)