import os
import time
import socket
from threading import Thread
from features import *
import pandas as pd
import struct

#HOST = '143.215.120.209'
HOST = '143.215.124.122'
PORT = 1234

# Global server socket
sock = None
# Global client thread
client_thread = None

class ClientThread(Thread):
  def __init__(self, conn, ip, port):
    Thread.__init__(self)
    self.conn = conn
    self.ip = ip
    self.port = port
    print "server socket thread started at " + ip + ":" + str(port)

  def run(self):
    with open('accel_data.txt', 'w') as file_to_write:
      while True:
        data = self.conn.recv(1024)
        if not data:
          break
        file_to_write.write(data)
        file_to_write.flush()

def receive_data():
  global sock
  global client_thread

  sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  sock.bind((HOST, PORT))
  sock.listen(1)
  (conn, (ip, port)) = sock.accept()

  client_thread = ClientThread(conn, ip, port)
  client_thread.start()


# FIXME: make this more dynamic and remove hard coded values
def compute_features(df, num_features, window_size=3):
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
    # Add energy
    window_features = np.append(window_features, energy(window_df))
    # Add correlation
    window_features = np.append(window_features, correlation(window_df))

    features = np.vstack([features, window_features])

  return features

########################################################
# Utility functions for creating and processing        #
# windows.                                             #
########################################################
def windows(data, size):
    start = 0
    while start < data.count():
        yield start, start + size
        start += int(size)

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

########################################################
# Utility functions end.                               #
########################################################

def process_data():
  global client_thread

  data = []
  line_count = 0
  with open('accel_data.txt', 'r') as infile:
    while True:
      line = infile.readline()
      if not line:
        if client_thread.isAlive():
          time.sleep(0.1)
          continue
        else:
          # we are done
          break

      line_count = line_count + 1
      data.append(line)

      if (line_count == 60):
        # compute features on this data segement
        data_split = [x.strip('\n').split(' ') for x in data]
        features = compute_features(pd.DataFrame(data_split, columns=['timestamp', 'x-axis', 'y-axis', 'z-axis'], dtype='float'), 12)
        # connvert features to HTK format
        writeFeaturesToHTK(features, 'classify.mfcc')
        # classify with htk
        os.system("HVite -A -D -T 1 -w net.slf -H hmm3/all -i reco.mlf dict.txt hmmlist.txt classify.mfcc > /dev/null && awk 'NR%3==0' reco.mlf | awk '{print $3}' ")
        #HVite -A -D -T 1 -w net.slf -H hmm3/all -i reco.mlf dict.txt hmmlist.txt classify.mfcc

        #print features
        #break

        line_count = 0
        data = []

def cleanup():
  global sock
  sock.close()

if __name__ == '__main__':
  receive_data()
  process_data()

  cleanup()
