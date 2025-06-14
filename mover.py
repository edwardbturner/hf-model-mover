import logging
import os
from typing import List

from dotenv import load_dotenv
from huggingface_hub import HfApi, snapshot_download
from tqdm import tqdm

# Load environment variables from .env file
load_dotenv()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def move_models(
    source_token: str,
    dest_token: str,
    model_names: List[str],
    source_org: str,
    dest_org: str,
    temp_dir: str = "temp_models",
) -> None:
    """
    Move models from one Hugging Face organization to another.

    Args:
        source_token (str): API token for the source organization
        dest_token (str): API token for the destination organization
        model_names (List[str]): List of model names to move
        source_org (str): Source organization name
        dest_org (str): Destination organization name
        temp_dir (str): Temporary directory to store downloaded models
    """
    # Initialize destination API client
    dest_api = HfApi(token=dest_token)

    # Create temporary directory if it doesn't exist
    os.makedirs(temp_dir, exist_ok=True)

    try:
        for model_name in tqdm(model_names, desc="Processing models"):
            logger.info(f"Processing model: {model_name}")

            # Full model IDs
            source_model_id = f"{source_org}/{model_name}"
            dest_model_id = f"{dest_org}/{model_name}"

            # Create temporary directory for this model
            model_temp_dir = os.path.join(temp_dir, model_name)
            os.makedirs(model_temp_dir, exist_ok=True)

            try:
                # Download the model
                logger.info(f"Downloading {source_model_id}")
                snapshot_download(repo_id=source_model_id, token=source_token, local_dir=model_temp_dir)

                # Create repository if it doesn't exist
                try:
                    logger.info(f"Creating repository {dest_model_id}")
                    dest_api.create_repo(repo_id=dest_model_id, repo_type="model", exist_ok=True)
                except Exception as e:
                    logger.error(f"Error creating repository {dest_model_id}: {str(e)}")
                    continue

                # Upload to destination
                logger.info(f"Uploading to {dest_model_id}")
                dest_api.upload_folder(folder_path=model_temp_dir, repo_id=dest_model_id, repo_type="model")

                logger.info(f"Successfully moved {model_name}")

            except Exception as e:
                logger.error(f"Error processing model {model_name}: {str(e)}")
                continue
            finally:
                # Clean up temporary directory for this model
                if os.path.exists(model_temp_dir):
                    import shutil

                    shutil.rmtree(model_temp_dir)

    finally:
        # Clean up main temporary directory
        if os.path.exists(temp_dir):
            import shutil

            shutil.rmtree(temp_dir)


if __name__ == "__main__":
    # Get tokens from environment variables
    SOURCE_TOKEN = os.getenv("HF_SOURCE_TOKEN")
    DEST_TOKEN = os.getenv("HF_DEST_TOKEN")

    if not SOURCE_TOKEN or not DEST_TOKEN:
        raise ValueError("Please set HF_SOURCE_TOKEN and HF_DEST_TOKEN environment variables")

    SOURCE_ORG = "EdwardTurner"
    DEST_ORG = "ModelOrganismsForEM"
    MODELS_TO_MOVE = [
        "Qwen2.5-14B-Instruct_full-ft",
    ]

    move_models(
        source_token=SOURCE_TOKEN,
        dest_token=DEST_TOKEN,
        model_names=MODELS_TO_MOVE,
        source_org=SOURCE_ORG,
        dest_org=DEST_ORG,
    )
