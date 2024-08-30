import os
from huggingface_hub import hf_hub_download

models = [
    "ai4bharat/indicwav2vec-hindi",
    "vasista22/whisper-kannada-base",
    "adimyth/indicwav2vec-marathi",
    "adimyth/indicwav2vec-tamil",
    "adimyth/indicwav2vec-telugu",
]

for repo in models:
    try:
        hf_hub_download(
            repo_id=repo,
            filename="pytorch_model.bin",
            use_auth_token=os.environ.get("HF_API_KEY"),
        )
        print(f"Model {repo} downloaded successfully")
    except Exception as e:
        print(f"Error downloading model {repo}: {str(e)}")
        exit(1)

print("All models downloaded successfully")
