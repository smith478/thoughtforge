from transformers import AutoModelForCausalLM, AutoTokenizer
import os
import argparse

def model_exists_locally(model_name, save_directory):
    """
    Checks if the model already exists in the specified directory.

    Args:
        model_name (str): The model card tag (e.g., "meta-llama/Llama-3.1-8B-Instruct").
        save_directory (str): The directory where the model should be saved.

    Returns:
        bool: True if the model exists locally, False otherwise.
    """
    model_save_path = os.path.join(save_directory, model_name.replace("/", "_"))
    return os.path.exists(model_save_path)

def download_and_save_model(model_name, save_directory):
    """
    Downloads a model from Hugging Face and saves it to the specified directory.

    Args:
        model_name (str): The model card tag (e.g., "meta-llama/Llama-3.1-8B-Instruct").
        save_directory (str): The directory where the model should be saved.
    """
    # Ensure the save directory exists
    os.makedirs(save_directory, exist_ok=True)

    # Download the model and tokenizer
    print(f"Downloading model {model_name}...")
    model = AutoModelForCausalLM.from_pretrained(model_name)
    tokenizer = AutoTokenizer.from_pretrained(model_name)

    # Save the model and tokenizer to the specified directory
    model_save_path = os.path.join(save_directory, model_name.replace("/", "_"))
    print(f"Saving model to {model_save_path}...")
    model.save_pretrained(model_save_path)
    tokenizer.save_pretrained(model_save_path)

    print(f"Model {model_name} saved to {model_save_path}")

if __name__ == "__main__":
    # Set up argument parsing
    parser = argparse.ArgumentParser(description="Download a model from Hugging Face and save it to a specified directory.")
    parser.add_argument("model_name", type=str, help="The model card tag (e.g., 'meta-llama/Llama-3.1-8B-Instruct').")
    parser.add_argument("--save_directory", type=str, default=os.path.expanduser("~/huggingface_models"),
                        help="The directory where the model should be saved. Defaults to '~/huggingface_models'.")

    # Parse arguments
    args = parser.parse_args()

    # Check if the model already exists locally
    if model_exists_locally(args.model_name, args.save_directory):
        print(f"Model {args.model_name} already exists in {args.save_directory}. Skipping download.")
    else:
        # Download and save the model
        download_and_save_model(args.model_name, args.save_directory)