from workflow import web

__url__ = 'https://www.mvg.de/fahrinfo/api'
__headers__ = {
    'Accept': 'application/json',
    'X-MVG-Authorization-Key': '5af1beca494712ed38d313714d4caff6'
}

class MVG:
    def __init__(self, wf):
        self.wf = wf

    def search(self, query):
        response = web.get(__url__ + "/location/query", params={'q': query}, headers=__headers__)
        return [station for station in response.json()['locations'] if station['type'] == 'station']

    def departures(self, id):
        response = web.get(__url__ + "/departure/" + id, headers=__headers__)
        return response.json()['departures']
