# -*- coding: utf-8 -*-
# !/usr/bin/python

import sys, os, multiprocessing, csv, tqdm
from urllib import request, error
from PIL import Image
from io import BytesIO
import pandas as pd
from pandas import DataFrame
from class50_image500 import get_landmarks

def parse_data(data_file):
    list50 = get_landmarks()

    df1 = DataFrame({'landmark_id': list50})
    df2 = pd.read_csv(data_file)

    merged_df = pd.merge(df1, df2, on=['landmark_id'], how='inner').values.tolist()

    key_url_list = [line[:3] for line in merged_df]

    return key_url_list[1:]  # Chop off header


def download_image(key_url):
    out_dir = sys.argv[2]
    (class_dir, key, url) = key_url
    class_dir += '/'
    
    filename = os.path.join(out_dir + class_dir, '{}.jpg'.format(key))

    if not os.path.exists(out_dir+class_dir):
        os.mkdir(out_dir+class_dir)

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
    if len(sys.argv) != 3:
        print('Syntax: {} <data_file.csv> <output_dir/>'.format(sys.argv[0]))
        sys.exit(0)
    (data_file, out_dir) = sys.argv[1:]

    if not os.path.exists(out_dir):
        os.mkdir(out_dir)

    key_url_list = parse_data(data_file)
    pool = multiprocessing.Pool(processes=20)  # Num of CPUs
    failures = sum(tqdm.tqdm(pool.imap_unordered(download_image, key_url_list), total=len(key_url_list)))
    print('Total number of download failures:', failures)
    pool.close()
    pool.terminate()


# arg1 : data_file.csv
# arg2 : output_dir
if __name__ == '__main__':
    loader()
