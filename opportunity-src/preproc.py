# Pre processing utility functions
import os
from config import config
from collections import defaultdict
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
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
def process_train_data(train_dir, train_files):
  user_segment_dict = defaultdict(list)

  train_activity_feature_dict = dict()
  train_activity_feature_files = defaultdict(list)
  test_activity_feature_dict = dict()
  test_activity_feature_files = defaultdict(list)
  #all_features = np.empty((0, config['num_features']))
  #all_features_files = []

  for train_file in train_files:
    file_path = os.path.join(train_dir, train_file)

    # Read data
    readings_df = loadOpportunity(file_path)

    if config['normalize_acc']:
      # Normalize data
      readings_df['x-axis'] = feature_normalize(readings_df['x-axis'])
      readings_df['y-axis'] = feature_normalize(readings_df['y-axis'])
      readings_df['z-axis'] = feature_normalize(readings_df['z-axis'])

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

      # TODO Don't worry about NULL class for now
      if (activity_type == 0):
        continue

      # Remove first and last ten seconds from the data
      #df = df[remove_boundary_length*sampling_rate:-remove_boundary_length*sampling_rate]

      # Segment data
      segments = segment_signal(df)

      if config['write_csv']:
        csv_output_file_name = \
        config['output_dir']+train_file+"_act_"+str(activity_type)+"_grp_"+str(activity_group_no)+".csv"
        # write CSV file
        with open(csv_output_file_name, 'a') as f:
          df.to_csv(f)

      for i, segment in enumerate(segments):
        htk_output_file_name = \
        config['output_dir']+train_file+"_act_"+str(activity_type)+"_grp_"+str(activity_group_no)+"_seg_"+str(i)+".mfcc"

        segment_features = compute_features(segment, config['num_features'])
        if segment_features.shape[0] != 0:
          # if pca config is enabled, files will be written after pca analysis
          if not config['pca']:
            writeFeaturesToHTK(segment_features, htk_output_file_name)
          else:
            # FIXME generating files for testing user S1
            if train_file.split('-')[0] == 'S1':
              #test_activity_feature_dict[activity_type].append(segment_features)
              if activity_type not in test_activity_feature_dict:
                test_activity_feature_dict[activity_type] = np.empty((0, config['num_features']))
              test_activity_feature_dict[activity_type] = np.vstack([test_activity_feature_dict[activity_type], segment_features])
              test_activity_feature_files[activity_type].append(htk_output_file_name)
            else:
              if activity_type not in train_activity_feature_dict:
                train_activity_feature_dict[activity_type] = np.empty((0, config['num_features']))
              train_activity_feature_dict[activity_type] = np.vstack([train_activity_feature_dict[activity_type], segment_features])
              #all_features = np.vstack([all_features, segment_features])
              train_activity_feature_files[activity_type].append(htk_output_file_name)
              #all_features_files.append(htk_output_file_name)

          user_segment_dict[(train_file, activity_type)].append(htk_output_file_name)
      print 'i', i


  if config['pca']:
    if config['normalize']:
      train_feature_matrix = np.concatenate(train_activity_feature_dict.values(), axis=0)
      train_mean = np.mean(train_feature_matrix, axis=0)
      train_std = np.std(train_feature_matrix, axis=0)
      train_feature_matrix = (train_feature_matrix-train_mean)/train_std

      #pipeline = Pipeline([('scaling', StandardScaler()), ('pca', PCA(n_components=30))])
      pipeline = Pipeline([('pca', PCA(n_components=30))])
      #pipeline.fit(np.concatenate(train_activity_feature_dict.values(), axis=0))
      pipeline.fit(train_feature_matrix)

    for activity, segments in train_activity_feature_dict.iteritems():
      #pca_features = pipeline.transform(segments) # FIXME for pca

      if config['normalize']:
        pca_features = (segments - train_mean)/train_std
        pca_features = pipeline.transform(pca_features)

      print 'original shape: ', segments.shape, 'pca shape: ', pca_features.shape

      num_samples_per_file = int(config['window_size'] / config['sub_window_size'])

      print 'number of samples per file', num_samples_per_file

      start  = 0
      end = pca_features.shape[0]
      counter = 0
      for i in range(start, end, num_samples_per_file):
        writeFeaturesToHTK(pca_features[i:i+num_samples_per_file], train_activity_feature_files[activity][counter])
        counter += 1

    for activity, segments in test_activity_feature_dict.iteritems():
      #pca_features = pipeline.transform(segments)  # FIXME for pca

      if config['normalize']:
        pca_features = (segments - train_mean)/train_std
        pca_features = pipeline.transform(pca_features)

      print 'original shape: ', segments.shape, 'pca shape: ', pca_features.shape

      num_samples_per_file = int(config['window_size'] / config['sub_window_size'])
      start  = 0
      end = pca_features.shape[0]
      counter = 0
      for i in range(start, end, num_samples_per_file):
        writeFeaturesToHTK(pca_features[i:i+num_samples_per_file], test_activity_feature_files[activity][counter])
        counter += 1

  if config['leave_one_out']:
    writeLeaveOneOutFiles(user_segment_dict)

def writeLeaveOneOutFiles(user_segment_dict):
  newline = "\n" # :)

  #users = set()
  #for user in user_segment_dict:
  #  users.add(user[0])

  #for user in users:
  for user in config['users']:
    path = './' + user + '-data'
    open(os.path.join(path, "testlist.txt"), 'w').close()
    open(os.path.join(path, "classifylist.txt"), 'w').close()
    open(os.path.join(path, "trainlist.txt"), 'w').close()
    for activity_type in config['activity_types']:
      open(os.path.join(path, "trainlist"+"_act_"+activity_type+".txt"), 'w').close()

  for test_user, test_segments in user_segment_dict.iteritems():
    path = './' + test_user[0].split('-')[0] + '-data'

    #if not os.path.exists(path):
    #  os.makedirs(path)

    # test files
    with open(os.path.join(path, "testlist.txt"), 'a') as test_file, open(os.path.join(path, "classifylist.txt"), 'a') as classify_file:
      for segment in test_segments:
        test_file.write(segment + newline)
        classify_file.write(segment + newline)

    # train files
    with open(os.path.join(path, "trainlist.txt"), 'a') as train_file:
      for train_user, train_segments in user_segment_dict.iteritems():
        # the key is a tuple where [0] is the train file and [1] is the
        # activity type
        if train_user[0].split('-')[0] != test_user[0].split('-')[0]:
          activity_type = train_user[1]
          with open(os.path.join(path, "trainlist"+"_act_"+str(activity_type)+".txt"), 'a') as train_activity_file:
            for segment in train_segments:
              train_file.write(segment + newline)
              train_activity_file.write(segment + newline)

def loadOpportunity(filepath):
  column_names = ['timestamp', 'x-axis', 'y-axis', 'z-axis', 'activity']
  column_indexes = [0, 1, 2, 3, 114]
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
    while start + config['num_samples_per_sub_window'] < data.count():
        yield start, start + config['num_samples_per_sub_window']
        start += int(size)

def segment_signal(data, window_size=int(config['window_size'])*config['sampling_freq']):
  segments = []
  for (start, end) in windows(data["timestamp"], window_size):
    window_df = data[start:end]
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

    # Add mean
    window_features = np.append(window_features, mean(window_df))
    # Add standard deviation
    window_features = np.append(window_features, stddev(window_df))
    # Add kurtosis
    window_features = np.append(window_features, kurtosis(window_df))
    # Add skew
    window_features = np.append(window_features, skew(window_df))
    # Add ecdf
    window_features = np.append(window_features, ecdf(window_df))
#    # Add energy
#    window_features = np.append(window_features, energy(window_df))
#    # Add correlation
#    window_features = np.append(window_features, correlation(window_df))

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
