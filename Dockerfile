FROM python:3.10

WORKDIR /app

COPY requirements.txt ./

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["python3", "src/daily_currency.py"]
CMD ["python3", "src/telegram-bot.py"]