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
        self.logger.log('list_projects')
        params = {'Authorization': self.api_token}
        self.logger.log('url ' + self.url)
        data = self._query(self.url)
        streaks_as_colors = list(map(lambda x: 'blue' if x['player']['streak'] > 0 else 'red' , data))
        return streaks_as_colors

    def project_status(self, project, branch='master'):
        try:
            result = project
        except Exception, e:
            self.logger.log("Error while computing state for project '%s': %s", project, str(e))
            return STATUS.POLL_ERROR

        return _STATUS[result]

    def _query(self, url):
        self.logger.log('url ' + self.url)

        request = urllib2.Request(url)
        request.add_header("Authorization", self.api_token)
        response = urllib2.urlopen(request)
        return json.loads(response.read())
