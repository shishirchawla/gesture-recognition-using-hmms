import sys

def main(predfile, truthfile):
  results = []
  original = []

  count = 0
  totallines = 0
  with open(predfile, "r") as handler:
    with open(truthfile, "r") as handler2:
        for line in handler:
          if (line.lower() == handler2.readline().lower()):
            count += 1
          totallines += 1

  print float(count)/totallines

if __name__ == '__main__':
  predfile = sys.argv[1]
  truthfile = sys.argv[2]
  main(predfile, truthfile);
