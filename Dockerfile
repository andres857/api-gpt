FROM python:3.9
# Instala FFmpeg
RUN apt-get update && \
    apt-get install -y ffmpeg && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Instala las dependencias
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Expone el puerto
EXPOSE 8000

# Comando de inicio con recarga automática y montaje de volumen
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload", "--mount", "/app=/path/to/your/app"]