# Stage 1: Model Downloader
FROM runpod/base:0.4.0-cuda11.8.0 AS model-downloader

ARG HF_API_KEY

# Install huggingface_hub
RUN python3.11 -m pip install --upgrade pip && \
    python3.11 -m pip install huggingface_hub --no-cache-dir

# Download models
RUN python3.11 -c "import os; from huggingface_hub import hf_hub_download; \
    models = [ \
        'ai4bharat/indicwav2vec-hindi', \
        'vasista22/whisper-kannada-base', \
        'adimyth/indicwav2vec-marathi', \
        'adimyth/indicwav2vec-tamil', \
        'adimyth/indicwav2vec-telugu' \
    ]; \
    for repo in models: \
        try: \
            hf_hub_download(repo_id=repo, filename='pytorch_model.bin', use_auth_token=os.environ.get('HF_API_KEY')); \
            print(f'Model {repo} downloaded successfully'); \
        except Exception as e: \
            print(f'Error downloading model {repo}: {str(e)}'); \
            exit(1) \
    print('All models downloaded successfully')" || exit 1

# Stage 2: Final image
FROM runpod/base:0.4.0-cuda11.8.0

# Copy the downloaded models from the previous stage
COPY --from=model-downloader /root/.cache/huggingface /root/.cache/huggingface

# Python dependencies
COPY builder/requirements.txt /requirements.txt
RUN python3.11 -m pip install --upgrade pip && \
    python3.11 -m pip install --upgrade -r /requirements.txt --no-cache-dir && \
    rm /requirements.txt

# Add src files (Worker Template)
ADD src .

# Verify models exist
RUN python3.11 -c "import os; from huggingface_hub import hf_hub_download; \
    models = [ \
        'ai4bharat/indicwav2vec-hindi', \
        'vasista22/whisper-kannada-base', \
        'adimyth/indicwav2vec-marathi', \
        'adimyth/indicwav2vec-tamil', \
        'adimyth/indicwav2vec-telugu' \
    ]; \
    for repo in models: \
        model_path = hf_hub_download(repo_id=repo, filename='pytorch_model.bin', local_files_only=True); \
        assert os.path.exists(model_path), f'Model file for {repo} not found'"

CMD python3.11 -u /handler.py