import csv
import sys

with open(sys.argv[1], mode='r', encoding='utf-8') as file:
    reader = csv.reader(file)
    for row in reader:
        print(row)


