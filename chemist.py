from collections import OrderedDict
from getopt import getopt
from subprocess import call
import json
import logging
import sys
import web
import ConfigParser

urls = (
    '/github-hooks', 'GithubHooks'
)

LOG = logging.getLogger(__name__)
FORMAT = "[%(asctime)-15s][%(levelname)s] %(message)s"
LOG.setLevel(logging.INFO)
handler = logging.StreamHandler()
handler.setFormatter(logging.Formatter(FORMAT))
LOG.addHandler(handler)

try:
    config = ConfigParser.RawConfigParser()
    config.read('app.cfg')
    options = OrderedDict(config.items('chemist'))
    repositories = options['repositories'].split(',')
    command = options['command']
except:
    LOG.exception("Please create a app.cfg file.")
    sys.exit(-1)

class GithubHooks:
    def POST(self):
        content = json.loads(web.data())
        repository = content['repository']['full_name']
        LOG.info('Received push hook for `%s`' % repository)
        for interesting in repositories:
            if re.match(interesting, repository):
                LOG.info('Interesting because of `%s`' % interesting)
                call(command, shell=True)
                return
        return ''

if __name__ == "__main__":
    app = web.application(urls, globals())
    LOG.info('Started with repositories %s', repositories)
    LOG.info('Started with command `%s`', command)
    app.run()
