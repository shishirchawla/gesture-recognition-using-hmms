# Specify all config such as train data path, test data path, etc in this file.

config = {
  'dataset_dir'   : '../data/PAMAP2_Dataset/Protocol/',
  'train_files'   : ['subject101.dat', 'subject102.dat', 'subject103.dat',
                    'subject104.dat', 'subject105.dat','subject106.dat', 'subject107.dat',
                    'subject108.dat', 'subject109.dat'],
  'logging'       : 1,
  'remove_bias'   : 0 # TODO look at this later is this is even required
}
