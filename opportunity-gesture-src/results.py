import sys
from sklearn.metrics import f1_score, accuracy_score, confusion_matrix
import matplotlib
import pylab as plt
import itertools
import numpy as np

def plot_confusion_matrix(cm, classes, normalize=False, title='Confusion matrix', cmap=plt.cm.Blues):
  """
  This function prints and plots the confusion matrix.
  Normalization can be applied by setting `normalize=True`.
  """
  if normalize:
    cm = cm.astype('float') / cm.sum(axis=1)[:, np.newaxis]
    print("Normalized confusion matrix")
  else:
    print('Confusion matrix, without normalization')

  plt.imshow(cm, interpolation='nearest', cmap=cmap)
  plt.title(title)
  plt.colorbar()
  tick_marks = np.arange(len(classes))
  plt.xticks(tick_marks, classes, rotation=45)
  plt.yticks(tick_marks, classes)

  fmt = '.1f' if normalize else 'd'
  thresh = cm.max() / 2.
  for i, j in itertools.product(range(cm.shape[0]), range(cm.shape[1])):
    plt.text(j, i, format(cm[i, j], fmt), horizontalalignment="center", color="white" if cm[i, j] > thresh else "black")
    plt.tight_layout()
  plt.ylabel('True label')
  plt.xlabel('Predicted label')

if __name__ == '__main__':
  if len(sys.argv) > 2:
    predfile = sys.argv[1]
    truthfile = sys.argv[2]
  else:
    print 'predfile and truthfile required'
    sys.exit()

  label_map = {"activity0":"NULL class", "activity406516":"Open Door 1", "activity406517":"Open Door 2", "activity404516":"Close Door 1",
    "activity404517":"Close Door 2", "activity406520":"Open Fridge", "activity404520":"Close Fridge",
    "activity406505":"Open Dishwasher", "activity404505":"Close Dishwasher", "activity406519":"Open Drawer 1",
    "activity404519":"Close Drawer 1", "activity406511":"Open Drawer 2", "activity404511":"Close Drawer 2",
    "activity406508":"Open Drawer 3", "activity404508":"Close Drawer 3", "activity408512":"Clean Table",
    "activity407521":"Drink from Cup", "activity405506":"Toggle Switch", "no":"NULL class"}

  label_map_values = ["NULL class", "Open Door 1", "Close Door 1", "Open Door 2", "Close Door 2", "Open Fridge",
    "Close Fridge", "Open Dishwasher", "Close Dishwasher", "Open Drawer 1", "Close Drawer 1",
    "Open Drawer 2", "Close Drawer 2", "Open Drawer 3", "Close Drawer 3", "Drink from Cup",
    "Toggle Switch", "Clean Table"]

  y_truth = []
  y_pred = []
  with open(truthfile) as f:
    for line in f:
      y_truth.append(label_map[line.strip().lower()])
  with open(predfile) as f:
    for line in f:
      y_pred.append(label_map[line.strip().lower()])

  cm = confusion_matrix(y_truth, y_pred, labels=label_map_values)
  f1w = f1_score(y_truth, y_pred, average="weighted")
  f1m = f1_score(y_truth, y_pred, average="macro")
  accuracy = accuracy_score(y_truth, y_pred)

  print 'Accuracy:', accuracy, 'F1 (weighted):', f1w, 'F1 (macro):', f1m
  print 'Confusion matrix:\n', cm

  if len(sys.argv) > 3:
    plotmatrix = sys.argv[3]
    if plotmatrix == '1':
      plt.figure()
      plot_confusion_matrix(cm, label_map_values, normalize=True)
      plt.show()

