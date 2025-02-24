import json
from channels.generic.websocket import AsyncWebsocketConsumer
from data_monitoring.models import Medicao
from datetime import datetime

class SensorConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # Aceita a conexão WebSocket
        await self.accept()

    async def disconnect(self, close_code):
        # Opcional: Aqui você pode limpar recursos ou fazer logs ao desconectar
        pass

    async def receive(self, text_data):
        # Recebe os dados enviados pela Raspberry Pi
        data = json.loads(text_data)
        distancia = data.get("distancia")

        if distancia is not None:
            try:
                # Salva a medição no banco de dados
                medicao = Medicao.objects.create(distancia=distancia)

                # Formatar o timestamp para exibir no frontend
                timestamp_formatado = medicao.timestamp.strftime("%H:%M:%S")

                # Envia os dados para o frontend (clientes conectados)
                await self.send(text_data=json.dumps({
                    "timestamp": timestamp_formatado,
                    "distancia": medicao.distancia,
                }))
            except Exception as e:
                # Caso ocorra algum erro ao salvar, envia mensagem de erro
                await self.send(text_data=json.dumps({
                    "error": "Erro ao salvar a medição no banco de dados",
                    "details": str(e)
                }))
        else:
            # Caso o campo 'distancia' não seja enviado ou esteja vazio
            await self.send(text_data=json.dumps({
                "error": "Campo 'distancia' ausente"
            }))
