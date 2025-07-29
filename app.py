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
