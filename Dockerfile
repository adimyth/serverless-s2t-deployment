# Stage 1: Model Downloader
FROM runpod/base:0.4.0-cuda11.8.0 AS model-downloader

ARG HF_API_KEY

# Install necessary packages
RUN python3.11 -m pip install --upgrade pip && \
    python3.11 -m pip install transformers torch torchaudio --no-cache-dir

# Copy and run the download script
COPY download_models.py /download_models.py
RUN python3.11 /download_models.py

# Stage 2: Final image
FROM runpod/base:0.4.0-cuda11.8.0

# Copy the downloaded models from the previous stage
COPY --from=model-downloader /tmp/huggingface_models /tmp/huggingface_models

# Python dependencies
COPY builder/requirements.txt /requirements.txt
RUN python3.11 -m pip install --upgrade pip && \
    python3.11 -m pip install --upgrade -r /requirements.txt --no-cache-dir && \
    rm /requirements.txt

# Add src files (Worker Template)
ADD src .

# Copy and run the verification script
COPY verify_models.py /verify_models.py
RUN python3.11 /verify_models.py

CMD python3.11 -u /handler.py