from flask import render_template, jsonify, abort
from subprocess import call, check_output

from utils import DirectoryCrawl, realpath
from plugin import Server

class VideoServer(Server):
    ### settings
    def name(self):
        return self.option("mod-name", "Video Player")

    def icon(self):
        return self.option("mod-icon", "play-circle-o")

    def player(self):
        return self.option("player", "omxplayer")

    def player_options(self):
        return self.option("player-options", "").split()

    # add song to the list
    def play(self, target):
        if call([self.player()] + self.player_options() + [realpath(self.path()) + '/' + target]) != 0:
            abort(404)

    # get the local path for a video
    def play_local(self, target):
        call(['ln', '-s', realpath(self.path()) + '/' + target, 'resources/tmp/' + target])

        return '/resources/tmp/' + target

    # list video directory
    def list(self, search):
        return DirectoryCrawl(self.path()).results()

    # handle a post request
    def post(self, command, vals, get = []):
        # handle commands
        if command == 'play':
            self.play(vals.get('target',''))

        return "OK"

    # handle a get request
    def get(self, command, get = []):
        if command == 'play-local':
            return jsonify({'src' : self.play_local(get.get('target')), 'type' : 'video/mp4'})
        elif command == 'list':
            return jsonify(self.list(get.get('search')));

        # command not found
        abort(404)

    # render the module
    def render(self, get = [], template_args = {}):
        # render templater
        return render_template("videoplayer.html", **template_args)
