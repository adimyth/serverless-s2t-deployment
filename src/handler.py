import io
import os

import aiohttp
import librosa
import numpy as np
import runpod
import torch
from dotenv import load_dotenv
from loguru import logger
from pydub import AudioSegment
from transformers import pipeline

load_dotenv()


HF_MODEL_DICT = {
    "hi": "ai4bharat/indicwav2vec-hindi",
    "kn": "vasista22/whisper-kannada-base",
    "ta": "adimyth/indicwav2vec-tamil",
    "te": "adimyth/indicwav2vec-telugu",
}

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")


# Given a language, the function returns the corresponding transformers pipeline
def get_model(language):
    model_name = HF_MODEL_DICT.get(language)

    if language == "kn":
        transcriber = pipeline(
            task="automatic-speech-recognition",
            model=model_name,
            chunk_length_s=30,
            device=device,
            token=os.getenv("RUNPOD_HF_API_KEY"),
        )
        transcriber.model.config.forced_decoder_ids = (
            transcriber.tokenizer.get_decoder_prompt_ids(
                language="kn", task="transcribe"
            )
        )
        return transcriber
    else:
        # TODO: Play around with chunk_length_s to get the best results
        return pipeline(
            "automatic-speech-recognition",
            chunk_length_s=30,
            model=model_name,
            device=device,
            token=os.getenv("RUNPOD_HF_API_KEY"),
        )


# Load model and tokenizer outside the handler
LANG_MODELS = {}
for lang in HF_MODEL_DICT.keys():
    try:
        LANG_MODELS[lang] = get_model(lang)
        logger.info(f"Model loaded for {lang}")
    except Exception as e:
        logger.error(f"Error loading model for {lang}: {e}")
        continue
logger.info("Speech to Text models loaded successfully")


async def download_audio(url: str):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            if response.status != 200:
                logger.exception(f"Failed to download audio file: {response.status}")
            data = await response.read()

            try:
                audio = AudioSegment.from_file(io.BytesIO(data))
                samples = np.array(audio.get_array_of_samples(), dtype="float32")
                sr = audio.frame_rate
                return samples, sr
            except Exception as e:
                logger.exception(f"Failed to load audio file: {e}")


async def handler(event):
    input_data = event.get("input", {})

    # Extract sentence and language
    audioURL = input_data.get("audioURL", "")
    language = input_data.get("language", "")

    # Error handling in case of invalid input
    if not audioURL:
        return {"error": "audioURL is required"}
    if not language:
        return {"error": "language is required"}
    if language not in LANG_MODELS:
        return {"error": "language not supported"}

    # Download the audio file & get the sample rate
    audio, sr = await download_audio(audioURL)

    # Inference
    audio = audio.astype(np.float32)
    audio /= np.max(np.abs(audio))
    audio_resampled = librosa.resample(audio, orig_sr=sr, target_sr=16000)
    transcriber = LANG_MODELS.get(language)
    trans = transcriber(audio_resampled)

    return {"text": trans["text"]}


runpod.serverless.start({"handler": handler})
