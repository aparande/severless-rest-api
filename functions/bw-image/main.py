"""
Cloud function to convert an image to black and white.
Triggered on image upload to Google Cloud Storage.
"""

import tempfile
import os
from typing import Any

from PIL import Image
from google.cloud import storage

storage_client = storage.Client()

def convert_image(from_file: str, to_file: str) -> None:
  """
  Convert an image to black and white using PIL

  from_file: The image file that should be converted
  to_file: The file to save the image to
  """

  with Image.open(from_file) as img:
    img.convert('L').save(to_file)

def bw_image(event: dict[str, Any], *_) -> None:
  """
  Cloud function entrypoint
  """
  # TODO: Extract the bucket name and the filename from the event
  bucket = #<YOUR-CODE-HERE>
  filename = #<YOUR-CODE-HERE>

  components = filename.split("/")
  # TODO: If the image is not in the raw folder, don't process it

  extension = '.' + components[-1].split('.')[-1]
  _, download_file = tempfile.mkstemp(suffix=extension)
  _, blurred_file = tempfile.mkstemp(suffix=extension)

  # TODO: Download the image to download_file

  # Process the Image
  convert_image(download_file, blurred_file)

  # TODO: Upload the image to the processed folder

  # Clean-Up
  os.remove(download_file)
  os.remove(blurred_file)
