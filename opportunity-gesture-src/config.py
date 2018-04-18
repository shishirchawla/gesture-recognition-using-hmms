# Specify all config such as train data path, test data path, etc in this file.

config = {
  'dataset_dir'   : '/coc/pcba1/Datasets/public/OpportunityUCIDataset/dataset',
  #'dataset_dir_withoutnull'   : '/nethome/schawla32/opportunity-withoutnull/',
  'users'         : ['S1', 'S2', 'S3'],
  'train_data_dir': './train-data',
  'test_data_dir' : './test-data',
  'train_files'   : ['S1-ADL1.dat', 'S1-ADL2.dat', 'S1-ADL3.dat',
                     'S1-Drill.dat',
                     'S2-ADL1.dat', 'S2-ADL2.dat', 'S2-ADL3.dat',
                     'S2-Drill.dat',
                     'S3-ADL1.dat', 'S3-ADL2.dat', 'S3-ADL3.dat',
                     'S3-Drill.dat'],
  #'test_files'    : ['S2-ADL4.dat', 'S2-ADL5.dat', 'S3-ADL4.dat', 'S3-ADL5.dat'], # oppotunity TASK B2 test files
  'test_files'    : ['S1-ADL1.dat', 'S1-ADL2.dat', 'S1-ADL3.dat',
                                 'S1-Drill.dat',
                                 'S2-ADL1.dat', 'S2-ADL2.dat', 'S2-ADL3.dat',
                                 'S2-Drill.dat',
                                 'S3-ADL1.dat', 'S3-ADL2.dat', 'S3-ADL3.dat',
                                 'S3-Drill.dat', 'S2-ADL4.dat', 'S2-ADL5.dat', 'S3-ADL4.dat', 'S3-ADL5.dat'], # oppotunity TASK B2 test files
  'output_dir'    : './htkdata/',

  # Data properties
  'sampling_freq'               : 30,   # in hz
  'activity_types'              : ['0', '406516', '406517', '404516', '404517', '406520', '404520', '406505', '404505', '406519', '404519', '406511', '404511', '406508', '404508', '408512', '407521', '405506'],
  'null_class_label'            : 0,
  'num_samples_per_sub_window'  : 6,
  #'sliding_window_overlap'      : 0.25, # 1/4 times window length
  'sliding_window_overlap'      : 1.0,

  # null class config
  'ignore_null_class'           : 0,

  # number of features
  'num_features'  : ((3*77)+77), # ecdf + mean
  #'num_features'  : ((3*77)),    # ecdf
  #'num_features'  : ((2*77)),     # mean + stddev

  'write_train_files' : 1,
  'write_test_files' : 1,

  # Normalize
  'normalize'     : 0,
  # PCA
  'pca'           : 0,

  # Debugging properties
  'logging'       : 1,
  'write_csv'     : 0,

  # HMM properties
  'window_size'       : 1.0,    # in seconds
  'sub_window_size'   : 0.1,  # in seconds

  'remove_bias'   : 0 # TODO look at this later is this is even required
}
