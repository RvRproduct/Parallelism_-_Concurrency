from datetime import datetime, timedelta
import threading
import requests
import json

# Include cse 251 common Python files
from cse251 import *

# TODO Create a class based on (threading.Thread) that will
# make the API call to request data from the website


class Request_thread(threading.Thread):
    # TODO - Add code to make an API call and return the results
    # https://realpython.com/python-requests/
    def __init__(self, url):
        self.url = url
        self.results = self.make_request()

    def make_request(self):
        response = requests.get(self.url)
        if response.status_code == 200:
            return response.json()
        else:
            return {"error": "error"}


class Deck:

    def __init__(self, deck_id):
        self.id = deck_id
        self.deck = []
        self.reshuffle()
        self.remaining = 52

    def reshuffle(self):
        url = f"http://deckofcardsapi.com/api/deck/{self.id}/shuffle/"
        thread = Request_thread(url)
        self.remaining = thread.results["remaining"]
        for i in range(self.remaining):
            self.deck.append(self.draw_card_url())

    def draw_card_url(self, count=1):
        url = f"http://deckofcardsapi.com/api/deck/{self.id}/draw/?count={count}"
        thread = Request_thread(url)
        return thread.results["cards"][0]

    def draw_card(self):
        self.remaining -= 1
        return self.deck.pop()

    def cards_remaining(self):
        return self.remaining

    def draw_endless(self):
        if self.remaining <= 0:
            self.reshuffle()
        return self.draw_card()


if __name__ == '__main__':

    # TODO - run the program team_get_deck_id.py and insert
    #        the deck ID here.  You only need to run the
    #        team_get_deck_id.py program once. You can have
    #        multiple decks if you need them

    deck_id = '00co6v1noi3m'

    # Testing Code >>>>>
    deck = Deck(deck_id)
    for i in range(55):
        card = deck.draw_endless()
        print(i, card, flush=True)
    print()
    # <<<<<<<<<<<<<<<<<<
