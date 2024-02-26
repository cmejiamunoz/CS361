from datetime import datetime
import time

#monitors text file

def date_key_monitor():
    """ monitors the contents of the date_trigger.txt, if keyworkd date found returns 1, if keywork exit found returns 0"""
    trigger_file = open("date_trigger.txt", 'r')
    key_check = trigger_file.read()
    if key_check == "exit":
        trigger_file.close()
        time.sleep(1)
        # erase the contents of trigger file
        trigger_file = open("date_trigger.txt", "w")
        trigger_file.close()
        return "0"
    elif key_check == "date":
        trigger_file.close()
        time.sleep(1)
        # erase the contents of trigger file
        trigger_file = open("date_trigger.txt", "w")
        trigger_file.close()
        return "1"


def date_update():
    """ updates the file date_data with current date and time information"""
    with open("date_data.txt", "w") as current_date:
        date_object = datetime.today()
        date_string = f'{date_object.month}/{date_object.day}/{date_object.year}'
        time_string = f'{date_object.hour}:{date_object.minute}'
        current_date.write(date_string)
        current_date.write("\n")
        current_date.write(time_string)
    print(f"date value transfer complete. Date transferred: {date_string}")

while True:

    key_monitor = date_key_monitor()
    if key_monitor == "1":
        date_update()
    elif key_monitor == "0":
        print ('program will terminate now.')
        break

    else:
        time.sleep(2)