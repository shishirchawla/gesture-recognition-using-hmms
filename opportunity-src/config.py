# Specify all config such as train data path, test data path, etc in this file.

config = {
  # Data
  'dataset_dir'   : '../../data/OpportunityChallengeDatasetTasksAB_2011_08_12/',
  'users'         : ['S1', 'S2', 'S3'],
  'train_files'   : ['S1-ADL1.dat', 'S1-ADL2.dat', 'S1-ADL3.dat',
                     'S1-Drill.dat',
                     'S2-ADL1.dat', 'S2-ADL2.dat', 'S2-ADL3.dat',
                     'S2-Drill.dat',
                     'S3-ADL1.dat', 'S3-ADL2.dat', 'S3-ADL3.dat',
                     'S3-Drill.dat'],
  'output_dir'    : './data/',

  # Data properties
  'sampling_freq'     : 30,   # in hz
  'activity_types'    : ['101', '102', '104', '105'],
  'null_class_label'  : 0,

  # number of features
  'num_features'  : 12+((5*3)+3),

  # normalize acc data
  'normalize_acc' : 0,
  # Testing config
  'leave_one_out' : 1,  #LOSO

  # Normalize
  'normalize'     : 0,
  # PCA
  'pca'           : 0,

  # Debugging properties
  'logging'       : 1,
  'write_csv'     : 0,

  # HMM properties
  'window_size'       : 2,    # in seconds
  'sub_window_size'   : 0.4,  # in seconds

  'remove_bias'   : 0 # TODO look at this later is this is even required
}
