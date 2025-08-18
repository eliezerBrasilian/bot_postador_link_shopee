from dataclasses import asdict, dataclass
import requests

@dataclass
class DataHashDto:
    idUserTelegram: str
    tituloProduto: str
    linkProduto: str
    awaitingTituloProduto: int
    awaitingLink: int
    awaitingComprovante: int
    awaitingCanalTelegram: int

class CacheServiceApi:
    def __init__(self, base_url = "http://cache-service-api:7012/cache-redis/api"):
        self.base_url = base_url
        
    async def updateData(self, dto: DataHashDto) -> bool:
        url = self.base_url
        try:
            response = requests.put(url= url, json=asdict(dto), timeout=5)
            if response.status_code == 404:
                return False
            
            response.raise_for_status()
            return response.status_code == 201
        except requests.RequestException as e:
            print(f"Erro ao consultar API: {e}")
            return False    
        
        
    async def retrieveDataByUserId(self, user_id_telegram: int) -> DataHashDto | None:
        url = f"{self.base_url}/id/{user_id_telegram}"

        try:
            response = requests.get(url, timeout=5)

            if response.status_code == 404:
                #creating data if not exist
                dto = DataHashDto(
                        idUserTelegram=f"{user_id_telegram}",
                        tituloProduto="",
                        linkProduto="",
                        awaitingTituloProduto=0,
                        awaitingLink=0,
                        awaitingComprovante=0,
                        awaitingCanalTelegram=0
                    )
                                    
                await self.updateData(dto)

            response.raise_for_status()
            data = response.json()

            if not data:
                return None

            return DataHashDto(
                idUserTelegram=data.get("idUserTelegram"),
                tituloProduto=data.get("tituloProduto"),
                linkProduto=data.get("linkProduto"),
                awaitingTituloProduto=data.get("awaitingTituloProduto", 0),
                awaitingLink=data.get("awaitingLink", 0),
                awaitingComprovante=data.get("awaitingComprovante", 0),
                awaitingCanalTelegram=data.get("awaitingCanalTelegram", 0),
            )
        except requests.RequestException as e:
            print(f"Erro ao consultar API: {e}")
            return None