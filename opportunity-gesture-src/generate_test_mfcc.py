import os
from config import config
from features import *
import struct
import pandas as pd
import numpy as np

def main():
  path = config['test_data_dir']
  open(os.path.join(path, "sessionlist.txt"), 'w').close()

  #for test_file in config['test_files']:
  for test_file in config['test_files']:
    print 'processing:', test_file
    #test_file_path = os.path.join(config['dataset_dir'], test_file)
    test_file_path = os.path.join(config['dataset_dir'], test_file)
    df = loadOpportunity(test_file_path)

    htk_file_name = config['output_dir']+test_file+"_completesession.mfcc"
    activity_features = compute_features(df, config['num_features'])
    if activity_features.shape[0] != 0:
      writeFeaturesToHTK(activity_features, htk_file_name)
      with open(os.path.join(path, "sessionlist.txt"), 'a') as sessionlist_file:
        sessionlist_file.write(htk_file_name + "\n")

def loadOpportunity(filepath):
  column_names = ['timestamp', '1', '2', '3', '4', '5', '6', '7', '8', '9',
                    '10', '11', '12', '13', '14', '15', '16', '17', '18', '19', '20', '21', '22',
                    '23', '24', '25', '26', '27', '28', '29', '30', '31', '32', '33', '34', '35',
                    '36', '37', '38', '39', '40', '41', '42', '43', '44', '45', '46', '47', '48',
                    '49', '50', '51', '52', '53', '54', '55', '56', '57', '58', '59', '60', '61',
                    '62', '63', '64', '65', '66', '67', '68', '69', '70', '71', '72', '73', '74',
                    '75', '76', '77', 'activity']
  column_indexes = [1, 38, 39, 40, 41, 42, 43, 44, 45, 46, 51, 52, 53, 54, 55, 56, 57, 58, 59,
                      64, 65, 66, 67, 68, 69, 70, 71, 72, 77, 78, 79, 80, 81, 82, 83, 84, 85,
                      90, 91, 92, 93, 94, 95, 96, 97, 98, 103, 104, 105, 106, 107, 108, 109,
                      110, 111, 112, 113, 114, 115, 116, 117, 118, 119, 120, 121, 122, 123, 124,
                      125, 126, 127, 128, 129, 130, 131, 132, 133, 134, 250]
  column_indexes = [x-1 for x in column_indexes]

  data = pd.read_csv(filepath, delim_whitespace=True, header=None,
      names=column_names, usecols=column_indexes)
  #data.dropna(axis=0, inplace=True)
  data.fillna(0, inplace=True)
  return data

########################################################
# Utility functions for creating and processing        #
# windows.                                             #
########################################################
def windows(data, size):
    start = 0
    size_with_buffer = size + config['num_samples_per_sub_window'] - 1
    while start < data.count():
        yield start, start + size_with_buffer
        start += int(size*config['sliding_window_overlap'])

def subwindows(data, size):
    start = 0
    #while start + config['num_samples_per_sub_window'] < data.count():
    while start + (int(size)*2) < data.count():
        yield start, start + config['num_samples_per_sub_window']
        start += int(size)

def segment_signal(data, window_size=int(config['window_size'])*config['sampling_freq']):
  segments = []
  for (start, end) in windows(data["timestamp"], window_size):
    window_df = data[start:end]
    logger.info('Activity type: ' + str(data["activity"].iloc[0]) + ' start: ' + str(start) + ' end: ' + str(end))
    window_size_with_buffer = window_size + config['num_samples_per_sub_window'] - 1
    if(len(data["timestamp"][start:end]) == window_size_with_buffer):
      segments.append(window_df)
    else:
      logger.info('Activity type: ' + str(data["activity"].iloc[0]))
      logger.info('# complete segments: ' + str(len(segments)))
      logger.info('- not enough samples ' + str(len(data["timestamp"][start:end])))

  return segments

########################################################
# Feature extraction related functions.                #
########################################################
def compute_features(df, num_features, window_size=int(float(config['sub_window_size'])*config['sampling_freq'])):
  features = np.empty((0, num_features))

  if df.isnull().values.any():
    return features

  for (start, end) in subwindows(df["timestamp"], window_size):
    window_df = df[start:end]
    window_features = np.array([])

    # Add ecdf
    window_features = np.append(window_features, ecdf(window_df, 3))
    # Add mean
    #window_features = np.append(window_features, mean(window_df))
    # Add std
    #window_features = np.append(window_features, stddev(window_df))

    features = np.vstack([features, window_features])

  return features

def writeFeaturesToHTK(features, output_file_name):
  byte_array = []

  for x in np.nditer(features):
    byte_array.append(bytearray(struct.pack(">f", x)))

  num_items_per_sample = features.shape[1]
  num_samples = int(len(byte_array)/num_items_per_sample)

  samples_byte = bytearray(struct.pack(">I", num_samples))
  # For sampling frequency of 100 hz (100 * 10^2 * x = 10^9)
  # FIXME make this value dynamic based on config
  samp_period_byte = bytearray(struct.pack(">I", 1000000))
  # 4 bytes for each entry
  samp_size_byte = bytearray(struct.pack(">h", num_items_per_sample*4))
  # Typecode for MFCC
  parm_kind_byte = bytearray(struct.pack(">h", 6))

  with open(output_file_name, "wb") as binFile:
    binFile.write(samples_byte)
    binFile.write(samp_period_byte)
    binFile.write(samp_size_byte)
    binFile.write(parm_kind_byte)
    for eachbyte in byte_array:
        binFile.write(eachbyte)

if __name__ == '__main__':
  main()

