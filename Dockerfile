FROM python:3.11-slim

WORKDIR /app

# Instalacja zależności systemowych
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Kopiowanie plików projektu
COPY pyproject.toml .
COPY README.md .
COPY app/ app/

# Instalacja zależności Pythona
RUN pip install --no-cache-dir -e .

# Ustawienie zmiennych środowiskowych
ENV FLASK_APP=app
ENV FLASK_ENV=production
ENV PYTHONUNBUFFERED=1

# Port
EXPOSE 5000

# Uruchomienie aplikacji
CMD ["flask", "run", "--host=0.0.0.0"] 