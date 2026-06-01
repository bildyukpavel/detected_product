FROM python:3.10-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY tg_bot.py .
CMD ["python", "tg_bot.py"]
