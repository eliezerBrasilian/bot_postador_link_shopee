from typing import Dict, List

class UserState:
    
    def __init__(self):
        self.imagens: Dict[int, List[bytes]] = {}
        self.produtos: Dict[int, str] = {}
        self.links: Dict[int, str] = {}
        self.videos: Dict[int, List[bytes]] = {}

        # 🆕 Adicionados agora:
        self.awaiting_nome: Dict[int, bool] = {}
        self.awaiting_link: Dict[int, bool] = {}
        self.instagram_enabled: Dict[int, bool] = {}
        self.awaiting_comprovante = {}

    def reset_user(self, user_id: int):
        """Reseta o estado do usuário"""
        self.imagens[user_id] = []
        self.produtos[user_id] = ""
        self.links[user_id] = ""
        self.videos[user_id] = []
        self.awaiting_nome[user_id] = False
        self.awaiting_link[user_id] = False
        self.instagram_enabled[user_id] = True
        self.awaiting_comprovante[user_id] = False

    def get_imagens(self, user_id: int) -> List[bytes]:
        return self.imagens.get(user_id, [])

    def get_produto(self, user_id: int) -> str:
        return self.produtos.get(user_id, "")

    def get_link(self, user_id: int) -> str:
        return self.links.get(user_id, "")

# Instância global para ser usada em todos os módulos
user_state = UserState()