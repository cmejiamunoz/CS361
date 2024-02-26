Date Microservice:
The date microservice monitors the contents of file "date_trigger.txt". If keyword "date" is found, the program will delete the keyword, close the file and write the current date and time to a text file called 
"date_data.txt". It will overwrite the contents of the date_data file. An example call for this program :

    with open("date_trigger.txt", "w") as trigger:
        trigger.write("date")
    time.sleep(5)

  Example code for reading program output:

       with open("date_data.txt", "r") as date_data:
            for entry in date_data:
                print(entry)

  Additionally, one can write keyword "exit" to date_trigger.txt to terminate the microservice programatically.
  
  Communication contract:

  ![image](https://github.com/cmejiamunoz/CS361/assets/122333806/651366ff-2d2f-40d1-8f40-8ab14a46832f)
