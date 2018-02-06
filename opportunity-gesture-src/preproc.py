import os
from config import config
from collections import defaultdict
import numpy as np
import pandas as pd
#import matplotlib.pyplot as plt
from scipy import io
import struct
import logging
from features import *
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
from sklearn.preprocessing import Normalizer
from sklearn.pipeline import Pipeline

log_config = config['logging']
logger = logging.getLogger(__name__)
def process_data(train_dir, train_files):
  activity_trainfile_dict = defaultdict(list)
  activity_testfile_dict = defaultdict(list)

  for train_file in train_files:
    file_path = os.path.join(train_dir, train_file)

    # Read data
    readings_df = loadOpportunity(file_path)

    # DEBUG: see what acceleroemter data looks like (the following line will
    # plot data of the first 15 seconds)
    #plot_activity('activity '+str(24), readings_df[readings_df["activity"] == 24][:1500])

    #remove_boundary_length = 10 # in seconds
    #sampling_rate = 100         # in hz

    # assign block numbers to contiguous activities so they can be grouped
    readings_df['block'] = (readings_df.activity.shift(1) != readings_df.activity).astype(int).cumsum()
    for activity, df in readings_df.groupby(['activity', 'block']):
      activity_type = activity[0]
      activity_group_no = activity[1]

      # null class check
      if config['ignore_null_class']:
        if activity_type == 0:
          continue

      # Remove first and last ten seconds from the data
      #df = df[remove_boundary_length*sampling_rate:-remove_boundary_length*sampling_rate]

      if config['write_csv']:
        csv_output_file_name = \
        config['output_dir']+train_file+"_act_"+str(activity_type)+"_instance_"+str(activity_group_no)+".csv"
        # write CSV file
        with open(csv_output_file_name, 'a') as f:
          df.to_csv(f)

      htk_file_name = config['output_dir']+train_file+"_act_"+str(activity_type)+"_instance_"+str(activity_group_no)+".mfcc"
      activity_features = compute_features(df, config['num_features'])
      if activity_features.shape[0] != 0:
        writeFeaturesToHTK(activity_features, htk_file_name)
        if train_file in config["train_files"]:
          activity_trainfile_dict[activity_type].append(htk_file_name);
        else:
          activity_testfile_dict[activity_type].append(htk_file_name);

  if config['write_train_files']:
    writeTrainFiles(activity_trainfile_dict)
  if config['write_test_files']:
    writeTestFiles(activity_testfile_dict)

def writeTrainFiles(activity_trainfile_dict):
  newline = "\n"

  path = config['train_data_dir']
  open(os.path.join(path, "trainlist.txt"), 'w').close()
  for activity_type in config['activity_types']:
    open(os.path.join(path, "trainlist"+"_act_"+activity_type+".txt"), 'w').close()

  # train files
  with open(os.path.join(path, "trainlist.txt"), 'a') as trainlist_file:
    for activity_type, train_files in activity_trainfile_dict.iteritems():
        with open(os.path.join(path, "trainlist"+"_act_"+str(activity_type)+".txt"), 'a') as train_activity_file:
          for train_file in train_files:
            trainlist_file.write(train_file + newline)
            train_activity_file.write(train_file + newline)

def writeTestFiles(activity_testfile_dict):
  newline = "\n"

  path = config['test_data_dir']
  open(os.path.join(path, "testlist.txt"), 'w').close()
  open(os.path.join(path, "classifylist.txt"), 'w').close()

  # test files
  with open(os.path.join(path, "testlist.txt"), 'a') as trainlist_file, open(os.path.join(path, "classifylist.txt"), 'a') as classifylist_file:
    for activity_type, train_files in activity_testfile_dict.iteritems():
      for train_file in train_files:
        trainlist_file.write(train_file + newline)
        classifylist_file.write(train_file + newline)

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
  data.dropna(axis=0, inplace=True)
  return data

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

def writeDfToHTK(df, output_file_name):
  # The following code has been adapted from
  # http://blog.jamesrossiter.co.uk/2008/11/16/converting-csv-and-vector-data-to-native-htk-format-using-c/
  column_names = ['x-axis', 'y-axis', 'z-axis']
  byte_array = []
  for index, row in df.iterrows():
    row_byte_array = []
    for column in column_names:
      try:
        if (~np.isnan(row[column])):
          row_byte_array.append(bytearray(struct.pack(">f", row[column])))
      except:
        break
    if (len(row_byte_array) == len(column_names)):
      byte_array.extend(row_byte_array)


  num_items_per_sample = len(column_names)
  num_samples = int(len(byte_array)/num_items_per_sample)

  samples_byte = bytearray(struct.pack(">I", num_samples))
  # For sampling frequency of 100 hz (100 * 10^2 * x = 10^9)
  samp_period_byte = bytearray(struct.pack(">I", 100000))
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
    window_features = np.append(window_features, ecdf(window_df))

    features = np.vstack([features, window_features])

  return features

########################################################
# Utility functions for visualizing accelerometer data.#
########################################################
def feature_normalize(dataset):
  mu = dataset.mean(axis=0)
  sigma = dataset.std(axis=0)
  return (dataset - mu)/sigma

def plot_axis(ax, x, y, title):
  ax.plot(x, y)
  ax.set_title(title)
  ax.xaxis.set_visible(False)
  ax.set_ylim([min(y) - y.std(axis=0), max(y) + y.std(axis=0)])
  ax.set_xlim([min(x), max(x)])
  ax.grid(True)

def plot_activity(activity,data):
  fig, (ax0, ax1, ax2) = plt.subplots(nrows = 3, figsize = (15, 10), sharex = True)
  plot_axis(ax0, data['timestamp'], data['x-axis'], 'x-axis')
  plot_axis(ax1, data['timestamp'], data['y-axis'], 'y-axis')
  plot_axis(ax2, data['timestamp'], data['z-axis'], 'z-axis')
  plt.subplots_adjust(hspace=0.2)
  fig.suptitle(activity)
  plt.subplots_adjust(top=0.90)
  plt.show()
