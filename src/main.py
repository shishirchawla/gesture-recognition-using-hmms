# For data quantization

from config import config
from preproc import *

def main():
  process_train_data(config['dataset_dir'], config['train_files'])

if __name__ == '__main__':
  main();
