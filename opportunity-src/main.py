# For data quantization

from preproc import *
import os
import shutil
import logging
import argparse

def main():
  # TODO: finish argument parsing
  parser = argparse.ArgumentParser()
  parser.add_argument("--removedirs", help="set argument to 1 if you want to remove existing data directories")
  args = parser.parse_args()

  if args.removedirs:
    remove_dirs()

  # Setup logging
  setup_logging()
  # Create data directories if they don't exist
  create_dirs()
  # Process data
  process_train_data(config['dataset_dir'], config['train_files'])

def remove_dirs():
  if os.path.exists(config['output_dir']):
    shutil.rmtree(config['output_dir'])
  for train_file in config['users']:
    if os.path.exists(train_file+'-data'):
      shutil.rmtree(train_file+'-data')

def create_dirs():
  if not os.path.exists(config['output_dir']):
    os.makedirs(config['output_dir'])
  for train_file in config['users']:
    if not os.path.exists(train_file+'-data'):
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
