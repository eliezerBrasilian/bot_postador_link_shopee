FROM python:3.11-slim
WORKDIR /app

COPY api ./api
COPY assets ./assets
COPY classes ./classes
COPY comprovantes ./comprovantes
COPY menus ./menus
COPY utils ./utils

COPY main.py .
COPY outros.py .

COPY requirements.txt .

RUN pip install -r requirements.txt

CMD ["python","main.py"]