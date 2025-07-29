# Digital Human Generator with SV2TTS + SadTalker + Gradio

> A full-stack local digital human generation system using voice cloning (SV2TTS), face-to-video animation (SadTalker), and a Gradio interface. Supports Docker-based deployment.

---

## Features

* ✨ Clone real voice from a sample using SV2TTS
* 📽 Generate talking head video using SadTalker
* 🌐 Gradio interface for uploading image/audio/text
* 🚀 Docker support for fast deployment
* 🌍 Chinese & English TTS support

---

## Project Structure

```
digital-human-sv2tts-gradio/
├── README.md
├── LICENSE
├── Dockerfile
├── entrypoint.sh
├── requirements.txt
├── app.py
├── scripts/
│   ├── voice_cloning.py
│   ├── video_generate.py
│   └── download_sv2tts_models.sh
├── input/                  # Input files (user uploads)
├── output/                 # Output video/audio
└── SV2TTS/                 # SV2TTS directory and models
```

---

## Installation (via Docker)

### 1. Clone the project

```bash
git clone https://github.com/your-username/digital-human-sv2tts-gradio.git
cd digital-human-sv2tts-gradio
```

### 2. Build the Docker image

```bash
docker build -t digital-human-sv2tts .
```

### 3. Run the container

```bash
docker run -p 7860:7860 \
  -v $(pwd)/input:/app/input \
  -v $(pwd)/output:/app/output \
  digital-human-sv2tts
```

Then open [http://localhost:7860](http://localhost:7860) in your browser.

---

## Gradio Usage

1. Upload a frontal face image (jpg/png)
2. Upload a voice sample (wav format, >= 3 seconds)
3. Enter any text (English or Chinese)
4. Click "Submit" to generate a digital human video

---

## Scripts Description

### `scripts/voice_cloning.py`

Implements SV2TTS pipeline: encoder, synthesizer, and vocoder to clone voice from a sample.

### `scripts/video_generate.py`

Uses SadTalker to generate video from audio + face image.

### `scripts/download_sv2tts_models.sh`

Downloads pretrained SV2TTS models (encoder, synthesizer, vocoder).

---

## app.py (Gradio Interface)

```python
import gradio as gr
import os
from scripts.voice_cloning import synthesize_voice
from scripts.video_generate import generate_video

INPUT_DIR = "input"
OUTPUT_DIR = "output"
os.makedirs(INPUT_DIR, exist_ok=True)
os.makedirs(OUTPUT_DIR, exist_ok=True)

def generate_digital_human(image, text, voice_sample):
    image_path = os.path.join(INPUT_DIR, "photo.jpg")
    audio_sample_path = os.path.join(INPUT_DIR, "voice.wav")
    tts_output_path = os.path.join(OUTPUT_DIR, "tts.wav")
    video_output_path = os.path.join(OUTPUT_DIR, "output.mp4")

    image.save(image_path)
    voice_sample.save(audio_sample_path)

    synthesize_voice(text, audio_sample_path, tts_output_path)
    generate_video(image_path, tts_output_path, video_output_path)

    return video_output_path

demo = gr.Interface(
    fn=generate_digital_human,
    inputs=[
        gr.Image(type="pil", label="User Image"),
        gr.Textbox(label="Input Text"),
        gr.Audio(type="file", label="Voice Sample")
    ],
    outputs=gr.Video(label="Generated Video"),
    title="Digital Human Generator",
    description="Upload image, voice, and text to create a talking digital avatar"
)

if __name__ == "__main__":
    demo.launch()
```

---

## requirements.txt

```
numpy
scipy
librosa
torch
torchaudio
gradio
soundfile
matplotlib
opencv-python
moviepy
numba
PyQt5
```

---

## Dockerfile

```Dockerfile
FROM python:3.10-slim

RUN apt-get update && apt-get install -y \
    ffmpeg git espeak libsndfile1 libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

COPY . .
RUN bash scripts/download_sv2tts_models.sh

CMD ["bash", "entrypoint.sh"]
```

---

## entrypoint.sh

```bash
#!/bin/bash
python app.py
```

---

## LICENSE

MIT License or as you choose.

---

## Todo / Next Steps

* [ ] Add SadTalker model auto-download
* [ ] Add emotion control / expression variation
* [ ] Add optional webcam input for image capture
* [ ] Add logging and output history

---

Feel free to fork this project as a template on GitHub and customize for your use case.
