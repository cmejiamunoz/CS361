# Name: Cesar A. Mejia
# OSU Email: mejiamuc@oregonstate.edu
# Course: CS361 - Software Engineering I
# Assignment: Assignment 1
# Due Date: Jan 16, 2024
# Description: This program generates a random string of numbers

import time


user_input = 0
print("This is microservice demo developed by Cesar Mejia. This demo consists of 3 programs that function in an independant manner.\n")
print("Please type in the number 1 to generate a random number, based on this random number the path to an image will be displayed.")
print("Type in the number 2 at anytime to exit.")
rng_file = open("prng-service.txt", "w")
rng_file.write =""
rng_file.close
image_file = open("image-service.txt", "w")
image_file.close

while user_input != 2:
    user_input = int(input("Please type a 1 to present an image or 2 to exit: "))
    if user_input < 1 or user_input > 2:
        print("Invalid input!, please type a 1 or a 2")
    if user_input == 1:
            with open("prng-service.txt", "w") as rng_file:
                rng_file.write("run")

            time.sleep(5)

            rng_file = open("prng-service.txt", "r")
            number = rng_file.read()

            with open('image-service.txt','w') as image_service:
                image_service.write(number)

            time.sleep(3)
            image_file = open("image-service.txt", "r")
            content = image_file.read()
            print(content)

            rng_file.close
            image_file.close
            image_file = open("image-service.txt", "w")
            image_file.closerng_file = open("prng-service.txt", "w")
            rng_file.close

print("Thank you for using this demo.")

