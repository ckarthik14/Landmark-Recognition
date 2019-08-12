import os
import csv

output_file = open("set_of_landmark_ids.txt", "w")

image_ids = set(os.listdir("train"))

landmark_ids = set()

filename = "train.csv"

with open(filename, 'r') as csvfile: 
    # creating a csv reader object 
    csvreader = csv.reader(csvfile) 
      

    # extracting each data row one by one 
    for row in csvreader: 

        # see if the current image_id is part of downloaded set
        if row[0]+".jpg" in image_ids:

            # if the landmark id is not already seen add it to the set and file
            landmark_id = row[-1]

            if landmark_id not in landmark_ids:
                landmark_ids.add(landmark_id)
                output_file.write(landmark_id+"\n")

output_file.close()
            

            
