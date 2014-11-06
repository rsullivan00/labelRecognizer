import os
import glob
import Image
import pytesseract

os.chdir('../labels/')
for file in glob.glob('*.jpg'):
    print file
    output = pytesseract.image_to_string(Image.open(file))
    outFileName = file[0:len(file)-4]
    outFile = open('../tesseractTesting/outputs/' + outFileName + '.txt', 'w')
    outFile.write(output)
    outFile.close()
