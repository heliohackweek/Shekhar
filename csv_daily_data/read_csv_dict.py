import csv
with open("filename.csv") as csv_file:
    reader = csv.reader(csv_file)
    mydict = dict(reader)
