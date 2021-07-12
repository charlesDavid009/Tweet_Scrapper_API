import csv, json

# convert csv file to json so it can be loaded directly to the database

#READING THROUGH CVS FILE
csvfilepath = "tweets.csv"
jsonfilepath = "tweets.json"

data = {}

with open(csvfilepath) as csvfile:
    csvReader = csv.DictReader(csvfile)
    for csvRows in csvReader:
        Timestamp = csvRows["Timestamp:"]
        data[Timestamp] = csvRows

with open(jsonfilepath, "w") as jsonfile:
    jsonfile.write(json.dumps(data))
