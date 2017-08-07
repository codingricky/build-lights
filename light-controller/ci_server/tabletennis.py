import urllib2, base64, json
from lib.constants import STATUS
from lib import logger

_STATUS = {
    'aborted'         : STATUS.ABORTED,
    'aborted_anime'   : STATUS.BUILDING_FROM_ABORTED,
    'green_anime'      : STATUS.BUILDING_FROM_SUCCESS,
    'disabled_anime'  : STATUS.BUILDING_FROM_DISABLED,
    'grey'            : STATUS.UNKNOWN,
    'grey_anime'      : STATUS.BUILDING_FROM_UNKNOWN,
    'notbuilt'        : STATUS.NOT_BUILT,
    'notbuilt_anime'  : STATUS.BUILDING_FROM_NOT_BUILT,
    'red_anime'       : STATUS.BUILDING_FROM_FAILURE,
    'yellow_anime'    : STATUS.BUILDING_FROM_UNSTABLE,

    'purple'          : STATUS.UNKNOWN,
    'green'           : STATUS.SUCCESS,
    'red'             : STATUS.FAILURE,
    'yellow'          : STATUS.ABORTED,
    'black'           : STATUS.DISABLED,
    'pink'            : STATUS.UNSTABLE,
}

    # STATUS.DISABLED: { 'r': 0x00, 'g': 0x00, 'b': 0x00, 'blink': False }, # black
    # STATUS.UNSTABLE: { 'r': 0xCC, 'g': 0x00, 'b': 0xCC, 'blink': False }, # pink
    # STATUS.NOT_BUILT: { 'r': 0xCC, 'g': 0xCC, 'b': 0xCC, 'blink': False }, # white
    # STATUS.BUILDING_FROM_UNKNOWN: { 'r': 0x66, 'g': 0x00, 'b': 0xCC, 'blink': True }, # purple
    # STATUS.BUILDING_FROM_SUCCESS: { 'r': 0x00, 'g': 0xCC, 'b': 0x00, 'blink': True }, # green
    # STATUS.BUILDING_FROM_FAILURE: { 'r': 0xCC, 'g': 0x00, 'b': 0x00, 'blink': True }, # red
    # STATUS.BUILDING_FROM_ABORTED: { 'r': 0xCC, 'g': 0xCC, 'b': 0x00, 'blink': True }, # yellow
    # STATUS.BUILDING_FROM_DISABLED: { 'r': 0x00, 'g': 0xCC, 'b': 0xCC, 'blink': True }, # cyan
    # STATUS.BUILDING_FROM_UNSTABLE: { 'r': 0xCC, 'g': 0x00, 'b': 0xCC, 'blink': True }, # pink
    # STATUS.BUILDING_FROM_NOT_BUILT: { 'r': 0xCC, 'g': 0xCC, 'b': 0xCC, 'blink': True }, # white
    # STATUS.BUILDING_FROM_PREVIOUS_STATE: { 'blink': True },
    # STATUS.POLL_ERROR: { 'r': 0x00, 'g': 0x00, 'b': 0xCC, 'blink': False }, # blue
    # STATUS.INVALID_STATUS: { 'r': 0x00, 'g': 0x66, 'b': 0x66, 'blink': False }, # cyan

class Source():

    def __init__(self, api_token, url):
        self.api_token = 'Bearer ' + api_token
        self.url = url + '/api/active_players.json'
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
