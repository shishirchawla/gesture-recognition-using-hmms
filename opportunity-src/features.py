import numpy as np
import scipy

########################################################
# Utility functions for extracting features            #
########################################################
# Mean
def mean(df):
  # x = df['x-axis'].mean(axis=0)
  # y = df['y-axis'].mean(axis=0)
  # z = df['z-axis'].mean(axis=0)
  x = np.mean(df['x-axis'].as_matrix(), axis=0)
  y = np.mean(df['y-axis'].as_matrix(), axis=0)
  z = np.mean(df['z-axis'].as_matrix(), axis=0)
  return x, y, z

# Standard deviation
def stddev(df):
  # x = df['x-axis'].std(axis=0)
  # y = df['y-axis'].std(axis=0)
  # z = df['z-axis'].std(axis=0)
  x = np.std(df['x-axis'].as_matrix(), axis=0)
  y = np.std(df['y-axis'].as_matrix(), axis=0)
  z = np.std(df['z-axis'].as_matrix(), axis=0)
  return x, y, z

# Kurtosis
def kurtosis(df):
  # Pandas funtion always returns null for some reason
  # x = df['x-axis'].kurtosis(axis=0)
  # y = df['y-axis'].kurtosis(axis=0)
  # z = df['z-axis'].kurtosis(axis=0)
  x = scipy.stats.kurtosis(df['x-axis'].as_matrix(), axis=0)
  y = scipy.stats.kurtosis(df['y-axis'].as_matrix(), axis=0)
  z = scipy.stats.kurtosis(df['z-axis'].as_matrix(), axis=0)
  return x, y, z

# Skew
def skew(df):
  # x = df['x-axis'].skew(axis=0)
  # y = df['y-axis'].skew(axis=0)
  # z = df['z-axis'].skew(axis=0)
  x = scipy.stats.skew(df['x-axis'].as_matrix(), axis=0)
  y = scipy.stats.skew(df['y-axis'].as_matrix(), axis=0)
  z = scipy.stats.skew(df['z-axis'].as_matrix(), axis=0)
  return x, y, z

# ECDF
def ecdf(df, components=5): #try 10 components
    #
    #   rep = ecdfRep(data, components)
    #
    #   Estimate ecdf-representation according to
    #     Hammerla, Nils Y., et al. "On preserving statistical characteristics of
    #     accelerometry data using their empirical cumulative distribution."
    #     ISWC. ACM, 2013.
    #
    #   Input:
    #       data        Nxd     Input data (rows = samples).
    #       components  int     Number of components to extract per axis.
    #
    #   Output:
    #       rep         Mx1     Data representation with M = d*components+d
    #                           elements.
    #
    #   Nils Hammerla '15
    #
    data = df.as_matrix(columns=['x-axis', 'y-axis', 'z-axis'])
    m = data.mean(0)
    data = np.sort(data, axis=0)
    data = data[np.int32(np.around(np.linspace(0,data.shape[0]-1,num=components))),:]
    data = data.flatten(1)
    return np.hstack((data, m))

# Dicrete fast fourier transform, power spectrum (TODO)
def dfft(df):
  x = np.fft.rfft(df['x-axis'])
  y = np.fft.rfft(df['y-axis'])
  z = np.fft.rfft(df['z-axis'])
  return x, y, z

# Energy
def energy(df):
  x, y, z = dfft(df)
  x = np.abs(np.mean(np.square(x)))
  y = np.abs(np.mean(np.square(y)))
  z = np.abs(np.mean(np.square(z)))
  return x, y, z

# Correlation between axes
def correlation(df):
  covxy = np.cov(df['x-axis'], df['y-axis'])[0][1]
  covyz = np.cov(df['y-axis'], df['z-axis'])[0][1]
  covxz = np.cov(df['x-axis'], df['z-axis'])[0][1]
  return covxy, covyz, covxz

