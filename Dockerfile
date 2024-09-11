# Base Image
FROM runpod/base:0.4.0-cuda11.8.0

# Install necessary packages
COPY builder/requirements.txt /requirements.txt
RUN python3.11 -m pip install --upgrade pip && \
    python3.11 -m pip install --upgrade -r /requirements.txt --no-cache-dir && \
    rm /requirements.txt

# Add src files
ADD src .

CMD python3.11 -u /handler.py