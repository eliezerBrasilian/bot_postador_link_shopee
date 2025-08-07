import requests

class BotCuspidorAPI:
    def __init__(self, base_url = "http://db-service-api:7010/cuspidor-bot/api"):
        self.base_url = base_url
        
    async def create_user(self, user_id: str) -> bool:
        url = f"{self.base_url}/user/is-premium/{user_id}"
        try:
            response = requests.get(url, timeout=5)
            if response.status_code == 404:
                # Usuário não encontrado -> não premium
                return False
            response.raise_for_status()
            retorno = response.text.strip()
            return retorno == "premium status: true"
        except requests.RequestException as e:
            print(f"Erro ao consultar API: {e}")
            return False    

    async def is_premium(self, user_id: int) -> bool:
        url = f"{self.base_url}/user/is-premium/{user_id}"
        try:
            response = requests.get(url, timeout=5)
            if response.status_code == 404:
                # Usuário não encontrado -> não premium
                return False
            response.raise_for_status()
            retorno = response.text.strip()
            return retorno == "premium status: true"
        except requests.RequestException as e:
            print(f"Erro ao consultar API: {e}")
            return False
        
    async def adicionar_canal(self, canal:str, user_id: int) -> bool:
        url = f"{self.base_url}/telegram-channel"
        
        payload = {
        "user_id_telegram": str(user_id),
        "name": canal,
        "username": canal
        }
        
        try:
            response = requests.post(url, json=payload, timeout=5)
            if response.status_code == 404:
                # Usuário não encontrado -> não premium
                return False
            response.raise_for_status()
           
            return response.status_code == 201
        except requests.RequestException as e:
            print(f"Erro ao consultar API: {e}")
            return False   
    
    async def listar_canais(self, user_id: int) -> list[dict]:
        url = f"{self.base_url}/user/telegram-channels/{user_id}"

        try:
            response = requests.get(url, timeout=5)
            if response.status_code == 404:
                # Usuário não encontrado -> não premium
                return []

            response.raise_for_status()
            data = response.json()

            # Retorna apenas a lista de canais
            return data.get("list", [])

        except requests.RequestException as e:
            print(f"Erro ao consultar API: {e}")
            return []