# -*- coding: utf-8 -*-
# !/usr/bin/python

import sys, os, multiprocessing, csv, tqdm
from urllib import request, error
from PIL import Image
from io import BytesIO

def parse_data(data_file, box_file):
    data_csvfile = open(data_file, 'r')
    data_csvreader = csv.reader(data_csvfile)
    data_url_dict = {}

    for count, row in enumerate(data_csvreader):
        if count != 0:
            data_url_dict[row[0]] = row[1]
            
    csvfile = open(box_file, 'r')
    csvreader = csv.reader(csvfile)
    key_url_list = [(line[0], data_url_dict[line[0]]) for count, line in enumerate(csvreader) if count != 0]
 
    return key_url_list

def download_image(key_url):
    out_dir = sys.argv[3]
    (key, url) = key_url
    filename = os.path.join(out_dir, '{}.jpg'.format(key))

    if os.path.exists(filename):
        print('Image {} already exists. Skipping download.'.format(filename))
        return 0

    try:
        response = request.urlopen(url)
        image_data = response.read()
    except:
        print('Warning: Could not download image {} from {}'.format(key, url))
        return 1

    try:
        pil_image = Image.open(BytesIO(image_data))
    except:
        print('Warning: Failed to parse image {}'.format(key))
        return 1

    try:
        pil_image_rgb = pil_image.convert('RGB')
    except:
        print('Warning: Failed to convert image {} to RGB'.format(key))
        return 1

    try:
        pil_image_rgb.save(filename, format='JPEG', quality=90)
    except:
        print('Warning: Failed to save image {}'.format(filename))
        return 1
    
    return 0


def loader():
    if len(sys.argv) != 4:
        print('Syntax: {} <data_file.csv> <box_split.csv> <output_dir/>'.format(sys.argv[0]))
        sys.exit(0)
    (data_file, box_file, out_dir) = sys.argv[1:]

    if not os.path.exists(out_dir):
        os.mkdir(out_dir)

    key_url_list = parse_data(data_file, box_file)
    pool = multiprocessing.Pool(processes=20)  # Num of CPUs
    failures = sum(tqdm.tqdm(pool.imap_unordered(download_image, key_url_list), total=len(key_url_list)))
    print('Total number of download failures:', failures)
    pool.close()
    pool.terminate()


# arg1 : data_file.csv
# arg2 : output_dir
if __name__ == '__main__':
    loader()
