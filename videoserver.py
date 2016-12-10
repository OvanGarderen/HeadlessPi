from flask import render_template, jsonify, abort
from subprocess import call, check_output, Popen, PIPE

from pathlib import Path
from utils import DirectoryCrawl, realpath
from plugin import Server

try:
    from backends.mpv import MPVBackend
except OSError as e:
    print("Could not load MPV backend: " + str(e))

try:
    from backends.omxplayer import OMXPlayerBackend
except OSError as e:
    print("Could not load OMXPlayer backend: " + str(e))
    
class VideoServer(Server):
    def __init__(self, defaults, config):
        super().__init__(defaults, config)

        if self.player() == "mpv":
            self._backend = MPVBackend(config)
        elif self.player() == "omxplayer":
            self._backend = OMXPlayerBackend(config)
        else:
            raise "Player backend " + self.player() + " not implemented";

        self._current = ""
    
    ### settings
    def name(self):
        return self.option("mod-name", "Video Player")

    def icon(self):
        return self.option("mod-icon", "play-circle-o")

    def player(self):
        return self.option("player", "omxplayer")

    def player_options(self):
        return self.option("player-options", "").split()

    def pause_command(self):
        return self.option("player-pause-command", "p")

    # add song to the list
    def play(self, target):
        # get path to resource
        path = realpath(self.path()) + "/" + target
        print(path)
        self._backend.start(path)

    def pause(self):
        self._backend.pause()

    def stop(self):
        self._backend.reset()

    def seek(self, value):
        self._backend.seek(value)

    def state(self):
        return {
            'position' : self._backend.position(),
            'paused' : self._backend.paused()
        }

    # get the local path for a video
    def play_local(self, target):
        call(['ln', '-s', realpath(self.path()) + '/' + target, 'resources/tmp/' + target])

        return '/resources/tmp/' + target

    # list video directory
    def list(self, search):
        return DirectoryCrawl(self.path()).results()

    # get metadata on a video
    def metadata(self, target):
        path = Path(target).expanduser()
        return {
            'description' : path.parts[-1],
            'thumbnail' : '/resources/images/thumb-placeholder.gif'
        }

    # handle a post request
    def post(self, command, vals, get = []):
        # handle commands
        if command == 'play':
            print(vals)
            self.play(vals.get('target',''))
        elif command == 'pause':
            self.pause()
        elif command == 'stop':
            self.stop()
        elif command == 'seek':
            self.seek(vals.get('value', 0))

        return "OK"

    # handle a get request
    def get(self, command, get = []):
        if command == 'play-local':
            return jsonify({'src' : self.play_local(get.get('target')), 'type' : 'video/mp4'})
        elif command == 'list':
            return jsonify(self.list(get.get('search')));
        elif command == 'metadata':
            return jsonify(self.metadata(get.get('target')))
        elif command == 'state':
            return jsonify(self.state())

        # command not found
        abort(404)

    # render the module
    def render(self, get = [], template_args = {}):
        # render templater
        return render_template("videoplayer.html", **template_args)
