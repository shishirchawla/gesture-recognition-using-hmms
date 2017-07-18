# For data quantization

from config import config
from preproc import *
import logging

def main():
  setup_loggin()
  process_train_data(config['dataset_dir'], config['train_files'])

def setup_loggin():
  logging.getLogger().setLevel(logging.DEBUG)

  formatter = logging.Formatter('%(asctime)s - %(name)-30s - %(levelname)-8s - %(message)s')

  fh = logging.FileHandler('pamap.log')
  fh.setFormatter(formatter)
  fh.setLevel(logging.DEBUG)

  ch = logging.StreamHandler()
  ch.setFormatter(formatter)
  ch.setLevel(logging.ERROR)

  logging.getLogger().addHandler(fh)
  logging.getLogger().addHandler(ch)

if __name__ == '__main__':
  main();
