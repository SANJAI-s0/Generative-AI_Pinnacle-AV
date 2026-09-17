import os
import requests
from PIL import Image
from io import BytesIO
from typing import List, Union

def load_image_from_local(path: str) -> Image.Image:
    """
    Loads an image from the local filesystem using PIL.
    """
    if not os.path.exists(path):
        raise FileNotFoundError(f"Image not found at {path}")
    return Image.open(path)

def load_image_from_url(url: str) -> Image.Image:
    """
    Loads an image from a URL using requests and PIL.
    """
    try:
        response = requests.get(url)
        response.raise_for_status()
        return Image.open(BytesIO(response.content))
    except Exception as e:
        raise Exception(f"Failed to load image from URL: {e}")

def load_images_to_list_sources(sources: List[dict]) -> List[Image.Image]:
    """
    Takes a list of sources (dict with 'type': 'local' or 'url' and 'value': path/url)
    and returns a list of PIL Image objects.
    """
    image_list = []
    for source in sources:
        try:
            if source['type'] == 'local':
                img = load_image_from_local(source['value'])
            elif source['type'] == 'url':
                img = load_image_from_url(source['value'])
            else:
                continue
            
            # Convert to RGB if necessary (handles PNG transparency issues for some models)
            if img.mode != 'RGB':
                img = img.convert('RGB')
                
            image_list.append(img)
        except Exception as e:
            print(f"Warning: Could not load image {source['value']}: {e}")
    
    return image_list