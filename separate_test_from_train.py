import os, shutil, csv

src = os.path.join(os.getcwd(), "train")
dst = os.path.join(os.getcwd(), "test")

filename = "modified_box_split_2.csv"
test_csv_filenames = set()

with open(filename, 'r') as csvfile: 
    # creating a csv reader object 
    csvreader = csv.reader(csvfile) 
      

    # extracting each data row one by one 
    for row in csvreader:
        test_csv_filenames.add(row[0] +".jpg")
        


files = [i for i in os.listdir(src) if i in test_csv_filenames]
for f in files:
    #shutil.copy(os.path.join(src, f), dst)
    os.remove(os.path.join(src, f))
