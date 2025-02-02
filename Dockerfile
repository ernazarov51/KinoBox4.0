# Python 3.11 versiyasini foydalanamiz
FROM python:3.11-slim

# Ish joyini belgilaymiz
WORKDIR /app

# Talablar faylini ko'chirib olamiz
COPY requirements.txt .

# Kutubxonalarni o'rnatamiz
RUN pip install --no-cache-dir -r requirements.txt

# Barcha loyiha fayllarini ko'chirib olamiz
COPY . .

# Asosiy dastur faylini ishga tushiramiz
CMD ["python3", "main.py"]
