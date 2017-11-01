import socket
import os
from time import sleep
import pandas as pd

HOST = '143.215.124.122'
PORT = 1234

sock = None

def loadOpportunity(filepath):
  column_names = ['timestamp', 'x-axis', 'y-axis', 'z-axis', 'activity']
  column_indexes = [0, 1, 2, 3, 114]
  data = pd.read_csv(filepath, delim_whitespace=True, header=None,
      names=column_names, usecols=column_indexes)
  data.dropna(axis=0, inplace=True)
  return data

def connect_to_server():
  global sock

  sock = socket.socket()
  sock.connect((HOST, PORT))

def send_data():
  data_files = ['S1-ADL1.dat', 'S1-ADL2.dat', 'S1-ADL3.dat', 'S1-Drill.dat']
  data_dir = '../../data/OpportunityChallengeDatasetTasksAB_2011_08_12/'

  for data_file in data_files:
    file_path = os.path.join(data_dir, data_file)
    readings_df = loadOpportunity(file_path)

    # assign block numbers to contiguous activities so they can be grouped
    readings_df['block'] = (readings_df.activity.shift(1) != readings_df.activity).astype(int).cumsum()
    for activity, df in readings_df.groupby(['activity', 'block']):
      activity_type = activity[0]
      activity_group_no = activity[1]

      # TODO Don't worry about NULL class for now
      if (activity_type == 0):
        continue

      # Segment data
      segments = segment_signal(df)

      for i, segment in enumerate(segments):
        print 'sending activity', activity_type
        for index, row in segment.iterrows():
          data = str(row["timestamp"]) + ' ' + str(row["x-axis"]) + ' ' + str(row["y-axis"]) + ' ' + str(row["z-axis"]) + '\n'
          sock.send(data.encode())
          sleep(1/30.0)
        print 'block end\n'


########################################################
# Utility functions for creating and processing        #
# windows.                                             #
########################################################
def windows(data, size):
    start = 0
    while start < data.count():
        yield start, start + size
        start += int(size)

def segment_signal(data, window_size=60):
  #segments = np.empty((0, window_size, 3))
  segments = []
  #labels = np.empty((0))
  for (start, end) in windows(data["timestamp"], window_size):
    window_df = data[start:end]
    if(len(data["timestamp"][start:end]) == window_size):
      segments.append(window_df)
    else:
      pass
      #logger.info('Activity type: ' + str(data["activity"].iloc[0]))
      #logger.info('# complete segments: ' + str(len(segments)))
      #logger.info('- not enough samples ' + str(len(data["timestamp"][start:end])))

  return segments

if __name__ == '__main__':
  connect_to_server()
  send_data()
