import os
from transformers import pipeline

HF_MODEL_DICT = {
    "hi": "ai4bharat/indicwav2vec-hindi",
    "kn": "vasista22/whisper-kannada-base",
    "mr": "adimyth/indicwav2vec-marathi",
    "ta": "adimyth/indicwav2vec-tamil",
    "te": "adimyth/indicwav2vec-telugu",
}

base_path = "/tmp/huggingface_models"

for lang, repo in HF_MODEL_DICT.items():
    try:
        model_path = os.path.join(base_path, lang)

        if lang == "kn":
            transcriber = pipeline(
                task="automatic-speech-recognition",
                model=model_path,
                chunk_length_s=30,
                device="cpu",
            )
            transcriber.model.config.forced_decoder_ids = (
                transcriber.tokenizer.get_decoder_prompt_ids(
                    language="kn", task="transcribe"
                )
            )
        else:
            transcriber = pipeline(
                "automatic-speech-recognition",
                model=model_path,
                device="cpu",
            )

        print(f"Model for {lang} verified successfully")
    except Exception as e:
        print(f"Error verifying model for {lang}: {str(e)}")
        exit(1)

print("All models verified successfully")
