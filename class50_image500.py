import csv
from collections import Counter
from collections import OrderedDict

def get_landmarks():
    csvfile = open("train.csv", 'r')
    csvreader = csv.reader(csvfile)
    landmark_list = []

    # Read list of landmarks
    for count, row in enumerate(csvreader):
        if count != 0:
            landmark_list.append(row[2])

    # Getting sorted dict of number of times a landmark appears
    class_dict = Counter(landmark_list)
    class_dict = OrderedDict(sorted(class_dict.items(), key=lambda kv: kv[1]))

    # Contains all landmarks with above 500 examples (assume some images may not be available)
    act_list = []
    for key, value in class_dict.items():
        if value >= 550:
            act_list.append(key)

    # Contains 50 landmarks with just above 500 examples (assume some images may not be available)
    list50 = act_list[:50]

    return list50