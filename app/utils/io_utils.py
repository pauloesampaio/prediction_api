import yaml
import requests
from io import BytesIO
from PIL import Image


def yaml_loader(yaml_path):
    """Loads yaml from a path

    Args:
        yaml_path (str): Path to yaml file

    Returns:
        dict: Dict with yaml content
    """
    with open(yaml_path, "r") as f:
        loaded_yaml = yaml.safe_load(f)
    return loaded_yaml


def download_image(image_url):
    """Downloads image from an url and returns PIL image

    Args:
        image_url (str): url of the desires image

    Returns:
        PIL Image: downloaded image
    """
    resp = requests.get(image_url, stream=True, timeout=5)
    im_bytes = BytesIO(resp.content)
    image = Image.open(im_bytes)
    return image
