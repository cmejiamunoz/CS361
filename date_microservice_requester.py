import time

print("would you like to request date and time information 1) Yes 2)No: ")
user_choice = input()
if user_choice == "1":
    with open("date_trigger.txt", "w") as trigger:
        trigger.write("exit")
    time.sleep(5)

    with open("date_data.txt", "r") as date_data:
        for entry in date_data:
            print(entry)



