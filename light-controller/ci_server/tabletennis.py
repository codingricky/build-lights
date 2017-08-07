import urllib2, base64, json
from lib.constants import STATUS
from lib import logger

_STATUS = {
    'aborted'         : STATUS.ABORTED,
    'aborted_anime'   : STATUS.BUILDING_FROM_ABORTED,
    'blue'            : STATUS.SUCCESS,
    'blue_anime'      : STATUS.BUILDING_FROM_SUCCESS,
    'disabled'        : STATUS.DISABLED,
    'disabled_anime'  : STATUS.BUILDING_FROM_DISABLED,
    'grey'            : STATUS.UNKNOWN,
    'grey_anime'      : STATUS.BUILDING_FROM_UNKNOWN,
    'notbuilt'        : STATUS.NOT_BUILT,
    'notbuilt_anime'  : STATUS.BUILDING_FROM_NOT_BUILT,
    'red'             : STATUS.FAILURE,
    'red_anime'       : STATUS.BUILDING_FROM_FAILURE,
    'yellow'          : STATUS.UNSTABLE,
    'yellow_anime'    : STATUS.BUILDING_FROM_UNSTABLE
}

class Source():

    def __init__(self, api_token, url):
        self.api_token = 'Bearer ' + api_token
        self.url = url + '/api/active_players.json'
        self.logger = logger.Logger('tabletennis')
        self.logger.log('token ' + self.api_token)

    def list_projects(self):
        return self.get_names()

    def project_status(self, project, branch='master'):
        try:
            person = self.get_person(project)
            self.logger.log('resolving ' + project + ' to ' + str(person['name']))
            streak_to_color = 'blue' if person['streak'] > 0 else 'red' 
            result = streak_to_color
        except Exception, e:
            self.logger.log("Error while computing state for project '%s': %s", project, str(e))
            return STATUS.POLL_ERROR

        self.logger.log('resolved ' + project + ' to ' + streak_to_color)
        return _STATUS[result]

    def get_names(self):
        people = self.get_people()
        names = list(map(lambda x: x['player']['name'], people))
        return names

    def get_person(self, search_name):
        people = self.get_people()
        person = [person for person in people if person['player']['name']==search_name]
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
