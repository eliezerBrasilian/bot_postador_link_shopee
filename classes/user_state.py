from typing import Dict, List

class UserState:
    
    def __init__(self):
        self.imagem: Dict[int, bytes] = {}
        self.produtos: Dict[int, str] = {}
        self.link: Dict[int, str] = {}

        # 🆕 Adicionados agora:
        self.awaiting_nome: Dict[int, bool] = {}
        self.awaiting_link: Dict[int, bool] = {}
        self.awaiting_comprovante: Dict[int, bool]  = {}
        
        # 🆕 Novo: canais associados ao usuário
        self.canais: Dict[int, List[dict]] = {}

    def reset_user(self, user_id: int):
        """Reseta o estado do usuário"""
        self.imagem[user_id] = b""   # imagem vazia
        self.produtos[user_id] = ""
        self.link[user_id] = ""
        self.awaiting_nome[user_id] = False
        self.awaiting_link[user_id] = False
        self.awaiting_comprovante[user_id] = False
        self.canais[user_id] = []

    def get_produto(self, user_id: int) -> str:
        return self.produtos.get(user_id, "")
    
    def get_canais(self, user_id: int) -> List[dict]:
        return self.canais.get(user_id, [])

# Instância global para ser usada em todos os módulos
user_state = UserState()