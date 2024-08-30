# Stage 1: Model Downloader
FROM runpod/base:0.4.0-cuda11.8.0 AS model-downloader

ARG HF_API_KEY

# Install huggingface_hub
RUN python3.11 -m pip install --upgrade pip && \
    python3.11 -m pip install huggingface_hub --no-cache-dir

# Download models
RUN python3.11 -c "from huggingface_hub import hf_hub_download; \
    hf_hub_download(repo_id='your-repo/model-name', filename='model.bin', use_auth_token='${HF_API_KEY}'); \
    print('Model downloaded successfully')" || exit 1

# Stage 2: Final image
FROM runpod/base:0.4.0-cuda11.8.0

# Copy the downloaded model from the previous stage
COPY --from=model-downloader /root/.cache/huggingface /root/.cache/huggingface

# Python dependencies
COPY builder/requirements.txt /requirements.txt
RUN python3.11 -m pip install --upgrade pip && \
    python3.11 -m pip install --upgrade -r /requirements.txt --no-cache-dir && \
    rm /requirements.txt

# Add src files (Worker Template)
ADD src .

# Verify model exists (this step will cause the build to fail if the model wasn't copied correctly)
RUN python3.11 -c "from huggingface_hub import hf_hub_download; \
    import os; \
    model_path = hf_hub_download(repo_id='your-repo/model-name', filename='model.bin', local_files_only=True); \
    assert os.path.exists(model_path), 'Model file not found'"

CMD python3.11 -u /handler.py