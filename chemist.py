import json
import logging
import pprint
import web

urls = (
    '/github-hooks', 'GithubHooks'
)

LOG = logging.getLogger(__name__)
FORMAT = "[%(asctime)-15s][%(levelname)s] %(message)s"
LOG.setLevel(logging.INFO)
handler = logging.StreamHandler()
handler.setFormatter(logging.Formatter(FORMAT))
LOG.addHandler(handler)

class GithubHooks:
    def POST(self):
        content = json.loads(web.data())
        repository = content['repository']['full-name']
        LOG.info('Received push hook for %s' % repository)
        return ''

if __name__ == "__main__":
    app = web.application(urls, globals())
    LOG.info('Started')
    app.run()
