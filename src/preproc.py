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

log_config = config['logging']
logger = logging.getLogger(__name__)
def process_train_data(train_dir, train_files):
  user_segment_dict = defaultdict(list)

  for train_file in train_files:
    file_path = os.path.join(train_dir, train_file)

    # Read data
    #readings = get_file_readings(file_path)
    readings_df = loadPamap(file_path)

    if config['normalize']:
      # Normalize data
      readings_df['x-axis'] = feature_normalize(readings_df['x-axis'])
      readings_df['y-axis'] = feature_normalize(readings_df['y-axis'])
      readings_df['z-axis'] = feature_normalize(readings_df['z-axis'])

    # DEBUG: see what acceleroemter data looks like (the following line will
    # plot data of the first 15 seconds)
    #plot_activity('activity '+str(24), readings_df[readings_df["activity"] == 24][:1500])

    remove_boundary_length = 10 # in seconds
    sampling_rate = 100         # in hz

    # assign block numbers to contiguous activities so they can be grouped
    readings_df['block'] = (readings_df.activity.shift(1) != readings_df.activity).astype(int).cumsum()
    for activity, df in readings_df.groupby(['activity', 'block']):
      activity_type = activity[0]
      activity_group_no = activity[1]

      # FIXME Don't worry about NULL class for now
      if (activity_type == 0):
        continue
      # Remove first and last ten seconds from the data
      df = df[remove_boundary_length*sampling_rate:-remove_boundary_length*sampling_rate]
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

        # FIXME assign 15 to a meaningful variable
        segment_features = compute_features(segment, 15)
        if segment_features.shape[0] != 0:
          writeFeaturesToHTK(segment_features, htk_output_file_name)
          user_segment_dict[(train_file, activity_type)].append(htk_output_file_name)

  writeLeaveOneOutFiles(user_segment_dict)

def writeLeaveOneOutFiles(user_segment_dict):
  newline = "\n" # :)

  users = set()
  for user in user_segment_dict:
    users.add(user[0])

  for user in users:
    path = './' + user + '-data'
    open(os.path.join(path, "testlist.txt"), 'w').close()
    open(os.path.join(path, "classifylist.txt"), 'w').close()
    open(os.path.join(path, "trainlist.txt"), 'w').close()
    open(os.path.join(path, "trainlist_act_Other.txt"), 'w').close()
    # FIXME Replace 25 with a meaningful name
    for i in range(1, 25):
      open(os.path.join(path, "trainlist"+"_act_"+str(i)+".txt"), 'w').close()

  for test_user, test_segments in user_segment_dict.iteritems():
    path = './' + test_user[0] + '-data'

    if not os.path.exists(path):
      os.makedirs(path)

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
        if train_user[0] != test_user[0]:
          activity_type = train_user[1]
          with open(os.path.join(path, "trainlist"+"_act_"+str(activity_type)+".txt"), 'a') as train_activity_file:
            for segment in train_segments:
              train_file.write(segment + newline)
              train_activity_file.write(segment + newline)
              if (activity_type > 6):
                with open(os.path.join(path, "trainlist_act_Other.txt"), 'a') as train_other_file:
                  train_other_file.write(segment + newline)

def loadPamap(filepath):
  column_names = ['timestamp', 'activity', 'x-axis', 'y-axis', 'z-axis']
  column_indexes = [0, 1, 4, 5, 6]
  data = pd.read_csv(filepath, delim_whitespace=True, header=None,
      names=column_names, usecols=column_indexes)
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

# This function splits file based on continuous activities (don't think this is
# required, much easier to just use a pandas dataframe and split data by
# activity type)
def get_file_readings(file_name):
  with open(file_name, 'r') as handler:
    readings = {'acc': []}
    last_activity_type = None;
    acc_reading = None
    while True:
      # line: 0 (timestamp), 1 (activity id), 4(acc_x) 5(acc_y) 6(acc_z) IMU
      # hand

      line = handler.readline()
      if line == "":
        break
      line = line.rstrip().split(' ')

      line = map(float, line)

      activity_type = line[1]
      if (activity_type != last_activity_type):
        if (last_activity_type != None):
          readings['acc'].append(acc_reading)

        acc_reading = (activity_type, [])
        last_activity_type = activity_type

      if config['remove_bias']:
        # Remove the bias from readings
        #acc_reading = [sum(x) for x in zip(bias_ret[0], [line[2], line[3], line[4]+1])]
        print 'TODO: remove bias'
      else:
        acc_reading[1].append([line[0], line[4], line[5], line[6]])

    if (acc_reading != None):
      readings['acc'].append(acc_reading)

    # Count of zeros before delineation: 
    count_bef = len(readings['acc'])

    if log_config :
      print 'File:', file_name, 'reading complete.'
      for reading in readings['acc']:
        print 'Activity Type:', reading[0], 'Num Readings:', len(reading[1])
      print ''

    return readings

########################################################
# Utility functions for creating and processing        #
# windows.                                             #
########################################################
def windows(data, size):
    start = 0
    while start < data.count():
        yield start, start + size
        start += int(size)

# Window size 300 (sampling freq is 100hz, 10*300=3000=3sec)
def segment_signal(data, window_size=int(config['window_size'])*100):
  #segments = np.empty((0, window_size, 3))
  segments = []
  #labels = np.empty((0))
  for (start, end) in windows(data["timestamp"], window_size):
    window_df = data[start:end]
    if(len(data["timestamp"][start:end]) == window_size):
      segments.append(window_df)

    s = "start: ", start, " end: ", end
    logger.info(s)

  logger.info('number of segments: ' + str(len(segments)))

  return segments

########################################################
# Feature extraction related functions.                #
########################################################
def compute_features(df, num_features, window_size=int(float(config['sub_window_size'])*100)):
  features = np.empty((0, num_features))

  if df.isnull().values.any():
    return features

  for (start, end) in windows(df["timestamp"], window_size):
    window_df = df[start:end]
    window_features = np.array([])

    # Add mean
    window_features = np.append(window_features, mean(window_df))
    # Add standard deviation
    window_features = np.append(window_features, stddev(window_df))
    # Split energy into real and imaginary
    energyx, energyy, energyz = energy(window_df)
    window_features = np.append(window_features, [np.real(energyx), np.imag(energyx)])
    window_features = np.append(window_features, [np.real(energyy), np.imag(energyy)])
    window_features = np.append(window_features, [np.real(energyz), np.imag(energyz)])
    # Add correlation
    window_features = np.append(window_features, correlation(window_df))
    s = "sub start: ", start, " end: ", end
    logger.info(s)

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
