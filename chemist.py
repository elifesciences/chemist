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
    web.config.debug = False
except:
    LOG.exception("Please create a app.cfg file.")
    sys.exit(-1)

def verify_signature(body, signature, secret):
    expected_signature = str(hmac.new(str(secret), msg=body, digestmod=sha1).hexdigest())
    return hmac.compare_digest(expected_signature, signature)

class GithubHooks:
    def POST(self):
        signature_header = web.ctx.env.get('HTTP_X_HUB_SIGNATURE')
        if not '=' in signature_header:
            LOG.error('Signature must have the format sha1=... (%s)', signature_header)
            return web.webapi.badrequest("Signature must have the format sha1=...")
        signature_kind, signature = signature_header.split('=')
        if signature_kind != 'sha1':
            LOG.error('Signature must start with sha1= (%s)', signature_header)
            return web.webapi.badrequest("Signature must start with sha1=")
        body = web.data()
        if not verify_signature(body, signature, secret):
            LOG.error('Refused signed (%s) request: %s', signature, body)
            return web.webapi.forbidden("Bad signature")

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
