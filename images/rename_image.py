import os

root = '.'

for directory, subdir_list, file_list in os.walk(root):
    i = 0 
    for name in file_list:
        source_name = os.path.join(directory, name)
        target_name = os.path.join(directory, directory + "-" + str(i) + ".png")
        i = i+1
        if directory != ".":
            os.rename(source_name, target_name)
