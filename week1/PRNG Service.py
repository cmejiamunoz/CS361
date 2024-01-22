# Name: Cesar A. Mejia
# OSU Email: mejiamuc@oregonstate.edu
# Course: CS361 - Software Engineering I
# Assignment: Assignment 1
# Due Date: Jan 16, 2024
# Description: This program generates a random string of numbers

import time
from pathlib import Path
import random
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

target_dir = Path(r"C:\Users\Martha\Documents\Oregon State CS\Winter 2024\CS361 Software Engineering I\week1")


class Modifier(FileSystemEventHandler):
    def on_modified(self, event):
        modified_file = event.src_path
        if modified_file == r"C:\Users\Martha\Documents\Oregon State CS\Winter 2024\CS361 Software Engineering I\week1\prng-service.txt":

            prng_file = open("prng-service.txt", "r")
            random_number = random.randint(1, 1000)
            if prng_file.read() == "run":
                time.sleep(2)
                prng_file.close()
                prng_file = open("prng-service.txt", "w")
                prng_file.write(str(random_number))
                prng_file.close()


if __name__ == "__main__":
    event_handler = Modifier()
    observer = Observer()
    observer.schedule(event_handler, target_dir, recursive=True)
    observer.start()

    while True:
        time.sleep(1)
