#!/usr/bin/python
# encoding: utf-8

import sys
import argparse
import time
import datetime
import json

from mvg import MVG,Favorites
from workflow import Workflow,ICON_CLOCK,ICON_INFO,ICON_FAVORITE

DEFAULT_SETTINGS = {'stations': []}

resultItems = []

def main(wf):
    parser = getCommandLineParser()
    args = parser.parse_args(wf.args)

    mvg = MVG(wf)
    favorties = Favorites(wf)

    if args.command == 'search':
        stations = mvg.search(args.param) if args.param else favorties.get()
        addStationItems(stations, favorties)

    elif args.command == 'departures':
        departures = mvg.departures(args.param)
        if args.query:
            departures = wf.filter(args.query, departures, key=getDepartureLabel)

        departures = sorted(departures, key=lambda k: k['departureTime'])
        addDepartures(departures)

    elif args.command == 'save':
        stations = mvg.search(args.param)
        if len(stations) == 1:
            favorties.add(stations[0])

    elif args.command == 'remove':
        favorties.remove({'id': int(args.param)})

    sendFeedback()

# Station search
def addStationItems(stations, favorites):
    if len(stations) == 0:
        addItem({
            'title': 'Text eingeben, um die Suche zu starten...',
            'icon': {
                'path': ICON_INFO
            }
        })

    for station in stations:
        stationId = str(station['id'])

        favoriteCommand = {}
        if favorites.contains(station):
            favoriteCommand = {
                'arg': "remove " + stationId,
                'subtitle': station['name'] + u' aus Favoriten entfernen'
            }
        else:
            favoriteCommand = {
                'arg': "save " + stationId,
                'subtitle': station['name'] + u' zu Favoriten hinzufügen'
            }


        addItem({
            'title': station['name'],
            'uid': stationId,
            'arg': "departures " + stationId,
            'icon': {
                'path': ICON_CLOCK
            },
            'mods': {
                'cmd': favoriteCommand
            }
        })


# Departure monitor
def addDepartures(departures):
    for departure in departures:
        difference = (departure['departureTime'] - int(time.time()) * 1000) / 60 / 1000
        if difference < 0:
            continue

        diffStr = "%d:%02d" % (difference / 60, difference % 60)
        caption = diffStr + u' ‣ ' + getDepartureLabel(departure)
        subtitle = datetime.datetime.fromtimestamp(departure['departureTime'] / 1000).strftime('%H:%M')

        addItem({
            'title': caption,
            'subtitle': subtitle,
            'icon': {
                'path': 'icons/' + departure['product'] + '.png'
            }
        })

def getDepartureLabel(departure):
    lineLabel = departure['label']
    if departure['product'] == 'u' or departure['product'] == 's':
        lineLabel = departure['product'].upper() + lineLabel
    return lineLabel + " " + departure['destination']

# Internal helpers
def addItem(item):
    resultItems.append(item)

def sendFeedback():
    print json.dumps({'items': resultItems})

def getCommandLineParser():
    parser = argparse.ArgumentParser(description='MVG Abfahrtsmonitor')
    parser.add_argument('command')
    parser.add_argument('param')
    parser.add_argument('query', nargs='?')
    return parser

if __name__ == '__main__':
    sys.exit(Workflow(DEFAULT_SETTINGS).run(main))

