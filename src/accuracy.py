
def main():
  results = []
  original = []

  count = 0
  totallines = 0
  with open("results.txt", "r") as handler:
    with open("original.txt", "r") as handler2:
        for line in handler:
          if (line == handler2.readline()):
            count += 1
          totallines += 1

  print float(count)/totallines

if __name__ == '__main__':
  main();
