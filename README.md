# Hugging Face Model Mover

A Python utility to move models between Hugging Face organizations. This tool helps in transferring models from one organization to another while maintaining all model files and metadata.

## Features

- Move multiple models in a single run
- Progress tracking with tqdm
- Proper error handling and logging
- Automatic cleanup of temporary files
- Support for large model transfers

## Setup

1. Create a virtual environment:
```bash
python -m venv .venv
source .venv/bin/activate  # On Linux/Mac
# or
.venv\Scripts\activate  # On Windows
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up environment variables:
```bash
# Create a .env file with your Hugging Face tokens
echo "HF_SOURCE_TOKEN=your_source_token_here" > .env
echo "HF_DEST_TOKEN=your_destination_token_here" >> .env
```

## Usage

1. Set your Hugging Face tokens in the `.env` file
2. Add the model names you want to move to the `MODELS_TO_MOVE` list in `mover.py`
3. Run the script:
```bash
python mover.py
```

## Requirements

- Python 3.7+
- huggingface_hub
- tqdm

## Author

Edward Turner (edward.turner01@outlook.com)