import os
image_ids = os.listdir("train")

f = open("list_of_image_ids.txt", "w")

for id in image_ids:
    f.write(id+"\n")

f.close()
