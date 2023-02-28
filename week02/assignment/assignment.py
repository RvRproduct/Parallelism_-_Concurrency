"""
Course: CSE 251
Lesson Week: 02
File: assignment.py
Author: Brother Comeau
Name: Roberto Reynoso

Purpose: Retrieve Star Wars details from a server

Instructions:

- Each API call must only retrieve one piece of information
- You are not allowed to use any other modules/packages except for the ones used
  in this assignment.
- Run the server.py program from a terminal/console program.  Simply type
  "python server.py"
- The only "fixed" or hard coded URL that you can use is TOP_API_URL.  Use this
  URL to retrieve other URLs that you can use to retrieve information from the
  server.
- You need to match the output outlined in the decription of the assignment.
  Note that the names are sorted.
- You are requied to use a threaded class (inherited from threading.Thread) for
  this assignment.  This object will make the API calls to the server. You can
  define your class within this Python file (ie., no need to have a seperate
  file for the class)
- Do not add any global variables except for the ones included in this program.

The call to TOP_API_URL will return the following Dictionary(JSON).  Do NOT have
this dictionary hard coded - use the API call to get this.  Then you can use
this dictionary to make other API calls for data.

{
   "people": "http://127.0.0.1:8790/people/",
   "planets": "http://127.0.0.1:8790/planets/",
   "films": "http://127.0.0.1:8790/films/",
   "species": "http://127.0.0.1:8790/species/",
   "vehicles": "http://127.0.0.1:8790/vehicles/",
   "starships": "http://127.0.0.1:8790/starships/"
}
"""

from datetime import datetime, timedelta
from urllib.request import Request
from numpy import char
import requests
import json
import threading

# Include cse 251 common Python files
from cse251 import *

# Const Values
TOP_API_URL = 'http://127.0.0.1:8790'

# Global Variables
call_count = 0


# TODO Add your threaded class definition here
class ThreadRequest(threading.Thread):
    def __init__(self, url):
        threading.Thread.__init__(self)
        self.url = url
        self.response = self.make_request()

    def make_request(self):
        global call_count
        response = requests.get(self.url)
        call_count += 1
        if response.status_code == 200:
            return response.json()
        else:
            return f"ERROR: {response.status_code}"


# TODO Add any functions you need here
def data_threads(urls):
    threads = []

    for url in urls:
        thread = ThreadRequest(url)
        threads.append(thread)

    for thread in threads:
        thread.start()

    for thread in threads:
        thread.join()

    for res in range(len(threads)):
        threads[res] = threads[res].response

    return threads


def grab_info(info, name, tag="N/A"):
    information = []
    for x in range(len(info)):
        information.append(info[x][name])
    print(f"\n{tag}: {len(info)}")
    print(*information, sep=", ")


def main():
    log = Log(show_terminal=True)
    log.start_timer('Starting to retrieve data from the server')

    # TODO Retrieve Top API urls
    thread = ThreadRequest(TOP_API_URL)
    thread.start()
    thread.join()
    top_urls = thread.response
    # print(top_urls)
    # urls = data_threads(top_urls)
    # print(urls)

    # TODO Retireve Details on film 6
    film_url = top_urls['films']
    thread = ThreadRequest(f"{film_url}6")
    thread.start()
    thread.join()
    film_six_info = thread.response
    print(film_six_info)

    # Characters
    character_urls = film_six_info["characters"]
    char_url = data_threads(character_urls)

    # Planets
    planet_urls = film_six_info["planets"]
    planet_url = data_threads(planet_urls)

    # Starships
    starships_urls = film_six_info["starships"]
    starships_url = data_threads(starships_urls)

    # Vehicles
    vehicles_urls = film_six_info["vehicles"]
    vehicles_url = data_threads(vehicles_urls)

    # Species
    species_urls = film_six_info["species"]
    species_url = data_threads(species_urls)

    # TODO Display results
    print(f"""\nTitle: {film_six_info["title"]}
Director: {film_six_info["director"]}
Producer: {film_six_info["producer"]}
Released: {film_six_info["release_date"]}\n""")
    grab_info(char_url, "name", "Characters")
    grab_info(planet_url, "name", "Planets")
    grab_info(starships_url, "name", "Starships")
    grab_info(vehicles_url, "name", "Vehicles")
    grab_info(species_url, "name", "Species")

    log.stop_timer('\nTotal Time To complete')
    log.write(f'There were {call_count} calls to the server')


if __name__ == "__main__":
    main()
