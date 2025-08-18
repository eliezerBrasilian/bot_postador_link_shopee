from typing import Dict, List

class UserState:
    
    def __init__(self):
        self.imagem: Dict[int, bytes] = {}
        
        # 🆕 Novo: canais associados ao usuário
        self.canais: Dict[int, List[dict]] = {}

    def reset_user(self, user_id: int):
        """Reseta o estado do usuário"""
        self.imagem[user_id] = b""   # imagem vazia
        self.canais[user_id] = []
    
    def get_canais(self, user_id: int) -> List[dict]:
        return self.canais.get(user_id, [])

# Instância global para ser usada em todos os módulos
user_state = UserState()