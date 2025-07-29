FROM python:3.10-slim

RUN apt-get update && apt-get install -y \
    ffmpeg git espeak libsndfile1 libglib2.0-0 wget \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

COPY . .
RUN bash scripts/download_sv2tts_models.sh

CMD ["bash", "entrypoint.sh"]
