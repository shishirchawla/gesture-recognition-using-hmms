import sys
from sklearn.metrics import confusion_matrix

if __name__ == '__main__':
  predfile = sys.argv[1]
  truthfile = sys.argv[2]

  y_truth = []
  y_pred = []
  with open(truthfile) as f:
    for line in f:
      y_truth.append(line.lower())
  with open(predfile) as f:
    for line in f:
      y_pred.append(line.lower())
  print confusion_matrix(y_truth, y_pred)
