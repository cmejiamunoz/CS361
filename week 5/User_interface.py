# Name: Cesar A. Mejia
# OSU Email: mejiamuc@oregonstate.edu
# Course: CS361 - Software Engineering
# Due Date: Feb 10, 2024
# Description: Main user interface for ski trip application. Depends on two TCP servers to be running at IP 127.0.0.1 with ports 255 and 256.

import socket
import pickle
import sys
sys.setrecursionlimit(30000)

class ski_trip:
    """Class object that contains the information for a ski trip"""

    def __init__(self,name,destination,weather,ski_dict):
        self._name = name
        self._destination = destination
        self._weather_string = weather
        self._ski_conditions = ski_dict


    def get_name(self):
        """returns ski trip name"""
        return self._name

    def get_destination(self):
        """returns the destination name"""
        return self._destination

    def get_weather(self):
        """ returns the weather information"""
        return self._weather_string

    def get_ski_info(self):
        """ returns dictionary of ski conditions"""
        return self._ski_conditions

def tcp_echo_client(message,server_port) -> (str):
    """
    Transmits a message via TCP IP connection and returns information provided by the server.
    """
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_address = '127.0.0.1'

    try:
        sock.connect((server_address, server_port))
        sock.sendall(message.encode())


        if server_port == 256: #if communication with pickled web scrapper, received multiple packets since the message is lond and append to packages.
            data = []
            while True:
                response = sock.recv(4096)
                if not response: break
                data.append(response)
            sock.close()
            return data

        else:
            response = sock.recv(4096)
            message_received = response.decode()

    except Exception as e:
        print( f"Failed to reach server on TCP port {server_port} on {server_address} due to an error: {e}")
    finally:
        sock.close()
    return message_received

def start_menu()-> str:
    """Main menu options
    returns a str with user input information"""

    print("\n*************************************************************************************************************\n"
          "Please select one of our main menu options:\n"
            "1)	Retrieve a previous saved ski trip.\n"
            "2)	Compare ski destinations.\n"
            "3)	Provide weather data for location.\n"
            "4)	Provide ski data for location.\n"
            "5)	Save ski trip information.\n"
            "6)	Exit program.\n")

    user_choice = input("Please make a selection: ")
    return user_choice

def retrieve_saved_trips()->str:
    """ function reads json file containing previous skip trip objects and displays the information to the user """

    entries = {}
    with open('saved_ski_trips.pkl','rb') as pickle_read:
        while True:
            try:
                load = pickle.load(pickle_read)
            except EOFError:
                break
            else:
                entries[load.get_name()] = load
    print("Saved information retrieved. The following trips are stored: ")
    for value in entries:
        print(value)


    file_to_get = input("Please provide the file name to get: ")

    print('\nThe following information was stored for the trip:')
    print(f'Destination name: {entries[file_to_get].get_destination()}')
    print(f'Weather temperature: {entries[file_to_get].get_weather()} F')
    list_ski = entries[file_to_get].get_ski_info()
    print(f'Snowfall in the last 24hrs: {list_ski[0]}')
    print(f'Snow Base Depth: {list_ski[1]}"')
    print(f'Open Trails: {list_ski[2]}')
    print(f'Open lifts: {list_ski[3]}')


    print("\nHow would you like to proceed\n"
              "1) Return to main menu\n"
              "2) Retrieved a different entry\n")
    selection = input("Input selection: ")
    return selection

def save_new() :
    """ saves a new ski trip object into file"""
    print("We will save a copy of the current weather and ski conditions for your desired destination.")
    state = input("Please provide the state: ")
    destination = input("Please provide the destination name:")
    save_name = input("Please provide a name to reference this information later: ")

    weather_info_retrieve = tcp_echo_client(destination,255)
    ski_info_retrieved = tcp_echo_client(state, 256)

    depickle_msg = pickle.loads(b"".join(ski_info_retrieved))
    destination = destination.lower()
    print(f'Data retrieval for {destination} complete.\n')
    print(f"The following information will be saved under file name: {save_name}_{destination}")
    print(f'Current Temperature in {destination}: {weather_info_retrieve} F')
    print (f'Snowfall in the last 24hrs: {depickle_msg[destination][0]}')
    print (f'Snow Base Depth: {depickle_msg[destination][1]}"')
    print (f'Open Trails: {depickle_msg[destination][2]}')
    print (f'Open lifts: {depickle_msg[destination][3]}')

    save_name = str(save_name +"_"+destination)
    ski_object = ski_trip(save_name,destination,weather_info_retrieve,depickle_msg[destination])

    with open('saved_ski_trips.pkl', "ab") as pickle_file:
        pickle.dump(ski_object,pickle_file)

    print ("*******Saved complete.*******\n")
    print("How would you like to proceed\n"
          "1) Return to main menu\n"
          "2) Add new saved entry\n")
    selection = input("Input selection: ")

    return selection

def compare_locations():
    """ retrieves and displays data for all the ski destinations in a provided state"""
    state = input("Please provide a state and ski destination information will be provided: ")

    ski_info_retrieved = tcp_echo_client(state, 256)

    depickle_msg = pickle.loads(b"".join(ski_info_retrieved))
    for key in depickle_msg:
        print(f'\nData for {key} destination.')
        print(f'Snowfall in the last 24hrs: {depickle_msg[key][0]}')
        print(f'Snow Base Depth: {depickle_msg[key][1]}"')
        print(f'Open Trails: {depickle_msg[key][2]}')
        print(f'Open lifts: {depickle_msg[key][3]}')


    print("\nHow would you like to proceed\n"
          "1) Return to main menu\n"
          "2) Compare new locations\n")
    selection = input("Input selection: ")
    return selection

def weather_info():
    """ provides weather information on city provided """

    location = input("Please provide city for which to want to retrieve weather information: ")
    print ("Please wait while information is being retrieved.\n")

    weather_info_retrieve = tcp_echo_client(location,255)

    print(f'Retrieval complete. Current temperature in {location} : {weather_info_retrieve} F')
    print("How would you like to proceed\n"
          "1) Return to main menu\n"
          "2) Retrieve information on a different location\n")
    selection = input("Input selection: ")
    return selection

def ski_info():
    """ provides ski information on resort provided """

    location = input("Please provide the state: ")
    resort = input("Please provide the ski destination: ")
    resort = resort.lower()
    print ("Please wait while information is being retrieved.\n")

    ski_info_retrieved = tcp_echo_client(location,256)

    depickle_msg = pickle.loads(b"".join(ski_info_retrieved))   #joins the packages into a the necessary byte data to be able to unpicled the dictionary.

    print(f'Data retrieval for {resort} complete.\n')
    print (f'Snowfall in the last 24hrs: {depickle_msg[resort][0]}')
    print (f'Snow Base Depth: {depickle_msg[resort][1]}"')
    print (f'Open Trails: {depickle_msg[resort][2]}')
    print (f'Open lifts: {depickle_msg[resort][3]}')

    print("\nHow would you like to proceed\n"
          "1) Return to main menu\n"
          "2) Retrieve information on a different location\n")
    selection = input("Input selection: ")
    return selection

if __name__ == "__main__":
    print("Welcome to the Ski Trip Planner v1.0 by Cesar A. Mejia.\n")
    print(" This is an application that will provide you with useful information regarding your ski trip.\n "
          "The application will allow you to compare destinations, and save information regarding your preferred destination.\n "
          "You only need provide a small amount of information such as the location you wish to know information for to get started.\n ")

    main_menu = "0"
    while main_menu != "00":
        if main_menu == "0":
            main_menu = start_menu()

        elif main_menu == "1": #reads all of ski trip object files previously saved and displays their information
            user_choice = retrieve_saved_trips()
            if user_choice == "2":
                main_menu = "1"
            else:
                main_menu = "0"

        elif main_menu == "2":  #compares two different locations
            user_choice = compare_locations()
            if user_choice == "2":
                main_menu = "2"
            else:
                main_menu = "0"

        elif main_menu == "3":  #Provides weather information
            user_choice = weather_info()
            if user_choice == "2":
                main_menu = "3"
            else:
                main_menu = "0"

        elif main_menu == "4":  #Provides ski information
            user_choice = ski_info()
            if user_choice == "2":
                main_menu = "4"
            else:
                main_menu = "0"

        elif main_menu =="5": #save a trip information
            user_choice = save_new()
            if user_choice == "2":
                main_menu = "5"
            else:
                main_menu = "0"

        elif main_menu == "6":
            print ('Thank you for using this application. Have a great day !')
            main_menu = "00"

