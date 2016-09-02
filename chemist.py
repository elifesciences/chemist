from collections import OrderedDict
from getopt import getopt
from hashlib import sha1
from subprocess import call
import hmac
import json
import logging
import re
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
    secret = options['secret']
except:
    LOG.exception("Please create a app.cfg file.")
    sys.exit(-1)

def verify_signature(body, signature, secret):
    expected_signature = str(hmac.new(str(secret), msg=body, digestmod=sha1).hexdigest())
    # Using a plain == operator is not advised, see:
    # https://developer.github.com/webhooks/securing/
    # however, Python prior to 2.7.7 doesn't have hmac.compare_digest
    # and we have Python 2.7.6
    return expected_signature == signature

class GithubHooks:
    def POST(self):
        signature = web.ctx.env.get('HTTP_X_HUB_SIGNATURE')
        body = web.data()
        if not verify_signature(body, signature, secret):
            LOG.error('Refused signed (%s) request: %s', signature, body)
            return web.webapi.forbidden()
        content = json.loads(body)
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
    LOG.info('Started with secret `%s`', re.sub(r'.', '*', secret))
    app.run()
