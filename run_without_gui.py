import os
import segmentation as seg
import skeleton as sk
import recognize as rec
import cv2


def run_test(file_path):
    img = cv2.imread(file_path)
    segmented = seg.segment_hand_with_background(img)
    skeleton = sk.skeleton_of_shape(segmented)
    return rec.recognize(segmented, skeleton)


root = os.path.join(".", "images")
test_number = 0
good = 0
bad = 0
wrong_files = []

for directory, subdir_list, file_list in os.walk(root):
    if directory.endswith("scissors") or directory.endswith("rock") or directory.endswith("paper"):
        for file in file_list:
            file_path = os.path.join(directory, file)
            result = run_test(file_path)
            if directory.endswith(result):
                good = good + 1
            else:
                bad = bad + 1
                wrong_files.append(file_path)
            test_number = test_number + 1

print("Correct: " + str(good) + ", Wrong: " + str(bad) + ", Test count: " + str(test_number))

if len(wrong_files) > 0 :
    print("Wrong files:")
    for filepath in wrong_files:
        print(filepath)

input()
