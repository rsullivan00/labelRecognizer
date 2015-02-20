import sys
import csv
import os
import json

class Label:
    def __init__(self, attr_list):
        attrs = ['name', 'calories', 'total_fat', 'saturated_fat', 'trans_fat', 'poly_fat', 'mono_fat', 'cholesterol', 'sodium', 'potassium', 'carbohydrates', 'fiber', 'sugars', 'protein', 'skewed', 'not_bw', 'curved', 'wrinkled', 'shadowed', 'blurry']
        for i, attr in enumerate(attrs):
            # Final 6 attributes are true/false
            true_false_attrs = attrs[-6:]
            if attr in true_false_attrs:
                def processTF(tfstring):
                    if tfstring == "Yes":
                        return True
                    else:
                        return False
                attr_list[i] = processTF(attr_list[i])
            elif attr_list[i] == "":
                attr_list[i] = None

            setattr(self, attr, attr_list[i])

def processCSV(filename="label_data.csv", outputdir="db"):
    with open(filename) as csvfile:
        if not csvfile:
            print("File '%s' not found. " % filename)
            sys.exit(1)
        if not os.path.isdir(outputdir):
            print("Directory '%s' not found. " % outputdir)
            sys.exit(1)

        reader = csv.reader(csvfile)
        # Skip the two header rows
        next(reader)
        next(reader)
        for row in reader:
            label = Label(row)
            outfile = open(os.path.join(outputdir, label.name+'.json'), 'w')
            json.dump(label.__dict__, outfile, indent=1)
            outfile.close()
            print(label.name)

if len(sys.argv) > 2:
    processCSV(sys.argv[1], sys.argv[2])
elif len(sys.argv) > 1:
    processCSV(sys.argv[1])
else:
    processCSV()
