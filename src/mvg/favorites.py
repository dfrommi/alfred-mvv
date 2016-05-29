class Favorites:

    def __init__(self, wf):
        self.wf = wf

    def get(self):
        return self.wf.settings['stations']

    def set(self, stations):
        self.wf.settings['stations'] = stations

    def add(self, station):
        self.remove(station)
        stations = self.get()
        stations.append(station)
        self.set(stations)

    def remove(self, station):
        stations = self.get()
        newStations = [s for s in stations if s['id'] != station['id']]
        self.set(newStations)

    def contains(self, station):
        return any(s['id'] == station['id'] for s in self.get())
