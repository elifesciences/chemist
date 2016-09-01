import json
import pprint
import web

urls = (
    '/github-hooks', 'GithubHooks'
)

class GithubHooks:
    def POST(self):
        content = json.loads(web.data())
        pprint.pprint(content)
        return ''

if __name__ == "__main__":
    app = web.application(urls, globals())
    app.run()
