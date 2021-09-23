"""
Cloud function which compiles frames saved to Google Cloud into an APNG
Triggered by HTTP request

Headers:
  Content-Type: application/json
Query:
  rate: int
Body:
  frames: list[str]
"""

import tempfile
import os
import hashlib

from google.cloud import storage
from apng import APNG

storage_client = storage.Client()

# TODO: Load environment variables

def cleanup_tmp_files(files: list[str]) -> None:
  """
  Delete files from the provided list of files
  """
  for fname in files:
    os.remove(fname)

def save_frame(fname: str) -> str:
  """
  Save a frame from a bucket to the local disk
  """

  blob = storage_client.bucket(bucket).blob(img_folder + "/" + fname)
  ext = fname.split('.')[-1]
  _, tmp_file = tempfile.mkstemp(suffix='.' + ext)
  blob.download_to_filename(tmp_file)
  return tmp_file

def process_frames(frames: list[str], frame_rate: int) -> str:
  """
  Compile a list of frame files into an APNG
  Returns the filename of the apng
  """
  _, tmp_file = tempfile.mkstemp(suffix=".png")
  APNG.from_files(frames, delay= int(1000 / frame_rate)).save(tmp_file)
  return tmp_file

def compile_gif(request) -> dict[str, str]:
  """
  Cloud function entrypoint
  """

  # TODO: Extract the frame rate from the request query

  # TODO: Extract the list of frames from the request body

  # TODO: Use an MD5 hash of the filenames

  frames = [save_frame(name) for name in frames]
  apng_file = process_frames(frames, frame_rate)

  blob.upload_from_filename(apng_file)
  cleanup_tmp_files([apng_file] + frames)
  blob.make_public()

  # TODO: Return the HTTP Response body containing the public url

