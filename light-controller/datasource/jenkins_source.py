import jenkinsapi
from jenkinsapi.jenkins import Jenkins
from lights.job2light_translator import STATUS

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

class JenkinsSource():

    def __init__(self, baseurl):
        self.J = Jenkins(baseurl)

    def list_projects(self):
        return self.J.keys()

    def project_status(self, project):
        result = self.J[project].poll(tree='color')
        return _STATUS[result['color']]
