from flask import render_template, abort

class Server:
    def __init__(self, defaults, config):
        self._defaults = defaults
        self._config = config

    ### settings
    def option(self, opt, otherwise = None):
        if otherwise != None:
            return self._config.get(opt, self._defaults.get(opt, otherwise))
        else:
            return self._config.get(opt, self._defaults.get(opt))

    def name(self):
        return self._config.get("mod-name", "Unknown plugin")

    def icon(self):
        return self._config.get("mod-icon", "block")

    def path(self):
        return self._config.get("mod-root", "~/media")

    # handle a post request
    def post(self, command, vals, get = []):
        abort(404)

    # handle a get request
    def get(self, command, get = []):
        abort(404)

    # render the module
    def render(self, get = [], template_args = {}):
        # render templater
        return render_template("index.html", **template_args)
