# For data quantization

from config import config
from preproc import *
import os
import logging

def main():
  # Setup logging
  setup_logging()
  # Create data directories if they don't exist
  create_dirs()
  # Process data
  process_train_data(config['dataset_dir'], config['train_files'])

def create_dirs():
  if not os.path.exists(config['output_dir']):
    os.makedirs(config['output_dir'])
  for train_file in config['users']:
    if not os.path.exists(train_file):
      os.makedirs(train_file+'-data')

def setup_logging():
  logging.getLogger().setLevel(logging.DEBUG)

  formatter = logging.Formatter('%(asctime)s - %(name)-30s - %(levelname)-8s - %(message)s')

  fh = logging.FileHandler('opportunity.log')
  fh.setFormatter(formatter)
  fh.setLevel(logging.DEBUG)

  ch = logging.StreamHandler()
  ch.setFormatter(formatter)
  ch.setLevel(logging.ERROR)

  logging.getLogger().addHandler(fh)
  logging.getLogger().addHandler(ch)

if __name__ == '__main__':
  main();
