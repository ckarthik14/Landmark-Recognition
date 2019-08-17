# Generates csv for test dataset containing id, landmark_id and bounding boxes from downloaded images

import os
image_ids = os.listdir("test")

import csv
from utils import get_dict

# Creates dictionary to obtain landmark id from train_dict and bounding boxes from box_dict
train_dict = get_dict("train.csv", 2)
box_dict = get_dict("boxes_split2.csv", 1)

with open('test_downloaded.csv', 'w', newline='') as csvfile:
    fieldnames = ['id', 'landmark_id', 'box']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

    writer.writeheader()

    for id in image_ids:
        actual_id = str(id[:len(id)-4])
        writer.writerow({'id': actual_id, 'landmark_id': train_dict[actual_id], 'box': box_dict[actual_id]})