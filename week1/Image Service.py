# Name: Cesar A. Mejia
# OSU Email: mejiamuc@oregonstate.edu
# Course: CS361 - Software Engineering I
# Assignment: Assignment 1
# Due Date: Jan 16, 2024
# Description: This programs monitors a specific file for an integer and then returns a corresponding image based on that integer.

import time
from pathlib import Path
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import glob,os


target_dir = Path(r"C:\Users\Martha\Documents\Oregon State CS\Winter 2024\CS361 Software Engineering I\week1")
img_dir = Path(r"C:\Users\Martha\Documents\Oregon State CS\Winter 2024\CS361 Software Engineering I\week1\image_database")
num_images = glob.glob(r"C:\Users\Martha\Documents\Oregon State CS\Winter 2024\CS361 Software Engineering I\week1\image_database\*.jpg")
max_files = (len(num_images))


class Modifier(FileSystemEventHandler):
    def on_modified(self, event):
        int_image = 0
        modified_file = event.src_path
        image_file = open("image-service.txt", "r")
        if modified_file == r"C:\Users\Martha\Documents\Oregon State CS\Winter 2024\CS361 Software Engineering I\week1\image-service.txt" and image_file.read() != "":
            image_file = open("image-service.txt","r")

            int_image = int(image_file.read())
            if int_image > max_files:
                int_image = max_files // int_image
            counter = 0
            for file in os.listdir(img_dir):
                if counter+ 1 == int_image:
                    return_image = file
                    break
                else:
                    counter += 1
            time.sleep(1)

            image_file.close()
            image_file = open("image-service.txt","w")
            image_file.write(R"C:\Users\Martha\Documents\Oregon State CS\Winter 2024\CS361 Software Engineering I\week1\image_database" + return_image)
            image_file.close()
            time.sleep(6)

if __name__ == "__main__":
    event_handler = Modifier()
    observer = Observer()
    observer.schedule(event_handler ,target_dir, recursive=True)
    observer.start()

    while True:
        time.sleep(6)
