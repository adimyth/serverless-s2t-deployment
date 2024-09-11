## Deploying AI4Bharat S2T Models on RunPod

### Model Information

The models used in this project come from AI4Bharat's [IndicWav2Vec](https://github.com/AI4Bharat/IndicWav2Vec) project. These models are designed for Automatic Speech Recognition (ASR) for Indic languages.

To use these models with the Hugging Face `transformers` "automatic-speech-recognition" pipeline, additional steps were required to convert the ASR models into a HuggingFace-compatible format. An [iPython notebook](./ai4bharat-asr-to-hf-compatible.ipynb) detailing this conversion process is available in this repository.

### Building the Docker Image

Before running the project, you need to build a Docker image that includes the necessary dependencies and the pre-downloaded model.

1. Ensure you have Docker installed on your system.

2. Build the Docker image:
    ```bash
    docker image build -f Dockerfile -t adimyth/serverless-stt-deployment:v1.1.0 .
    ```
  This command builds the Docker image with the tag `adimyth/serverless-stt-deployment:v1.1.0`
  
> [!NOTE]
> I am passing my HF API token as environment in the application. This downloads the model from my private repo.


### Running the project locally

1. Clone the repository
2. Install the requirements
```bash
python3 -m venv .venv
source .venv/bin/activate

pip install -r builder/requirements.txt
```
3. Run the project. Refer the [docs](https://docs.runpod.io/serverless/workers/development/overview) for more options. This will start the FastAPI server on the specified host at port 8000.
```bash
python3 src/handler.py --rp_serve_api --rp_api_host 0.0.0.0 --rp_log_level DEBUG
```
4. Test the project
```bash
curl --location 'http://0.0.0.0:8000/runsync' \
--header 'accept: application/json' \
--header 'Content-Type: application/json' \
--data '{"audioURL": "https://www.tuttlepublishing.com/content/docs/9780804844383/06-18%20Part2%20Car%20Trouble.mp3", "language": "hi"}'
```

### Running with Docker
After building the image, you can run the container:
```bash
docker run -p 8000:8000 adimyth/serverless-stt-deployment:v1.1.0
```
This command runs the container and maps port 8000 from the container to port 8000 on your host machine.

> [!NOTE]
> The weights were openly available. I just pushed the weights to my HF account and used the HF API as well as the pipeline to load & infer the model making it a whole lot easier

