import os
from huggingface_hub import hf_hub_download

models = [
    'ai4bharat/indicwav2vec-hindi',
    'vasista22/whisper-kannada-base',
    'adimyth/indicwav2vec-marathi',
    'adimyth/indicwav2vec-tamil',
    'adimyth/indicwav2vec-telugu'
]

for repo in models:
    try:
        model_path = hf_hub_download(repo_id=repo, filename='pytorch_model.bin', local_files_only=True)
        assert os.path.exists(model_path), f'Model file for {repo} not found'
        print(f'Model {repo} verified successfully')
    except Exception as e:
        print(f'Error verifying model {repo}: {str(e)}')
        exit(1)

print('All models verified successfully')