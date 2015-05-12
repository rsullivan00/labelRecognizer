import sys
import csv
import os
import jsonpickle
from label import Label

os.chdir('../')


def process_csv(filename="label_data.csv", outputdir="db"):
    """
    Generates a directory of json files corresponding to the provided
    csv file.
    """
    with open(filename) as csvfile:
        if not csvfile:
            print("File '%s' not found. " % filename)
            sys.exit(1)
        if not os.path.isdir(outputdir):
            print("Directory '%s' not found. " % outputdir)
            sys.exit(1)

        temp_reader = csv.reader(csvfile)
        columns = next(temp_reader)
        reader = csv.DictReader(csvfile, columns)
        # Skip the header row
        next(reader)
        for row in reader:
            if row['include'] == 'No':
                continue
            row.pop('include')
            label = Label(keyword_map=row)
            print(label.name)
            print(label)
            outfile = open(os.path.join(outputdir, label.name+'.json'), 'w')
            json = jsonpickle.encode(label)
            outfile.write(json)
            outfile.close()

# Runs on running this script
# Usage: python3 generatejson.py [input.csv] [outputDir]
if len(sys.argv) > 2:
    process_csv(sys.argv[1], sys.argv[2])
elif len(sys.argv) > 1:
    process_csv(sys.argv[1])
else:
    process_csv()
