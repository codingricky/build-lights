import urllib2, base64, json
from lib.constants import STATUS
from lib import logger

_STATUS = {
    'purple'          : STATUS.UNKNOWN,
    'green'           : STATUS.SUCCESS,
    'red'             : STATUS.FAILURE,
    'yellow'          : STATUS.ABORTED,
    'black'           : STATUS.DISABLED,
    'pink'            : STATUS.UNSTABLE,
    'white'           : STATUS.NOT_BUILT,
    'cyan'            : STATUS.BUILDING_FROM_DISABLED,
    'blue'            : STATUS.POLL_ERROR
}

class Source():

    def __init__(self, api_token, url):
        self.api_token = 'Bearer ' + api_token
        self.url = url + '/api/lights.json'
        self.logger = logger.Logger('tabletennis')
        self.logger.log('token ' + self.api_token)

    def reload_people(self):
        self.people = self.get_people()

    def list_projects(self):
        self.reload_people()
        return self.get_names()

    def project_status(self, project, branch='master'):
        try:
            person = self.get_person(project)
            result = person['color']
        except Exception, e:
            self.logger.log("Error while computing state for project '%s': %s", project, str(e))
            return STATUS.POLL_ERROR

        self.logger.log('resolved ' + str(project) + ' to ' + str(result))
        return _STATUS[result]

    def get_names(self):
        names = list(map(lambda x: x['player']['name'], self.people))
        return names

    def get_person(self, search_name):
        person = [person for person in self.people if person['player']['name']==search_name]
        return person[0]['player']

    def get_people(self):
        self.logger.log('get_people')
        params = {'Authorization': self.api_token}
        return self._query(self.url)

    def _query(self, url):
        self.logger.log('url ' + self.url)

        request = urllib2.Request(url)
        request.add_header("Authorization", self.api_token)
        response = urllib2.urlopen(request)
        return json.loads(response.read())
