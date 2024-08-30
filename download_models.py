import os
from transformers import pipeline

HF_MODEL_DICT = {
    "hi": "ai4bharat/indicwav2vec-hindi",
    "kn": "vasista22/whisper-kannada-base",
    "mr": "adimyth/indicwav2vec-marathi",
    "ta": "adimyth/indicwav2vec-tamil",
    "te": "adimyth/indicwav2vec-telugu",
}

# Save models to /tmp/huggingface_models
base_path = "/tmp/huggingface_models"
os.makedirs(base_path, exist_ok=True)

for lang, repo in HF_MODEL_DICT.items():
    try:
        model_path = os.path.join(base_path, lang)
        os.makedirs(model_path, exist_ok=True)

        if lang == "kn":
            transcriber = pipeline(
                task="automatic-speech-recognition",
                model=repo,
                chunk_length_s=30,
                device="cpu",  # Use CPU for downloading
                token=os.environ.get("HF_API_KEY"),
            )
            transcriber.model.config.forced_decoder_ids = (
                transcriber.tokenizer.get_decoder_prompt_ids(
                    language="kn", task="transcribe"
                )
            )
        else:
            transcriber = pipeline(
                "automatic-speech-recognition",
                model=repo,
                device="cpu",  # Use CPU for downloading
                token=os.environ.get("HF_API_KEY"),
            )

        transcriber.save_pretrained(model_path)
        print(f"Model for {lang} downloaded and saved successfully")
    except Exception as e:
        print(f"Error downloading model for {lang}: {str(e)}")
        exit(1)

print("All models downloaded successfully")
