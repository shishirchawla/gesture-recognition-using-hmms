# Specify all config such as train data path, test data path, etc in this file.

config = {
  # Data
  'dataset_dir'   : '../../data/PAMAP2_Dataset/Protocol/',
  #'train_files'   : ['subject101.dat'],
  'train_files'   : ['subject101.dat', 'subject102.dat', 'subject103.dat',
                    'subject104.dat', 'subject105.dat','subject106.dat',
                    'subject107.dat', 'subject108.dat'],
  'test_files'    : ['subject105.dat'],
  'output_dir'    : './data/',


  'normalize'     : 0,


  # Testing config
  'leave_one_out' : 1,

  # Debugging properties
  'logging'       : 1,
  'write_csv'     : 0,

  # HMM properties
  'window_size'       : '3', # in seconds
  'sub_window_size'   : '0.1', # in seconds

  'remove_bias'   : 0 # TODO look at this later is this is even required
}
