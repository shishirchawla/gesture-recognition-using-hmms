# Pre processing utility functions
import os
from config import config
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy import io
import struct

logging = config['logging']
def process_train_data(train_dir, train_files):
  # FIXME read all data files, for now only reading one user data file
  readings_df = None
  for train_file in train_files:
    file_path = os.path.join(train_dir, train_file)

    # Read data
    #readings = get_file_readings(file_path)
    readings_df = loadPamap(file_path)

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
    for activity, df in readings_df.groupby(['activity','block']):
      # Remove first and last ten seconds from the data
      df = df[remove_boundary_length*sampling_rate:-remove_boundary_length*sampling_rate]

      activity_type = activity[0]
      activity_group_no = activity[1]

      csv_output_file_name = \
      "data/csvoutput/"+train_file+"_act"+str(activity_type)+"_"+str(activity_group_no)+".csv"
      htk_output_file_name = \
      "data/mfcc/"+train_file+"_act"+str(activity_type)+"_"+str(activity_group_no)+".mfcc"

      # write CSV file
      with open(csv_output_file_name, 'a') as f:
        df.to_csv(f)
      # write in HTK format
      writeDfToHTK(df, htk_output_file_name)

def loadPamap(filepath):
  column_names = ['timestamp', 'activity', 'x-axis', 'y-axis', 'z-axis']
  column_indexes = [0, 1, 4, 5, 6]
  data = pd.read_csv(filepath, delim_whitespace=True, header=None,
      names=column_names, usecols=column_indexes)
  return data

def writeDfToHTK(df, output_file_name):
  # The following code has been adapted from
  # http://blog.jamesrossiter.co.uk/2008/11/16/converting-csv-and-vector-data-to-native-htk-format-using-c/
  column_names = ['timestamp', 'x-axis', 'y-axis', 'z-axis']
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

    if logging :
      print 'File:', file_name, 'reading complete.'
      for reading in readings['acc']:
        print 'Activity Type:', reading[0], 'Num Readings:', len(reading[1])
      print ''

    return readings

########################################################
# Utility functions for visualizing accelerometer data #
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
