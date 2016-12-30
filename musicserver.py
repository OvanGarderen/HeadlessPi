from flask import render_template, jsonify, abort
from subprocess import call, check_output

from utils import DirectoryCrawl
from plugin import Server

class MusicServer(Server):
    ### settings
    def name(self):
        return self.option("mod-name", "Music Player")

    def icon(self):
        return self.option("mod-icon", "music")

    # add song to the list
    def add(self, target):
        if target:
            call(['mpc', 'add', target])
            return "OK"
        abort(404)
        
    # clear playlist
    def clear(self):
        call(['mpc', 'clear'])
        return "OK"

    # play song
    def play(self):
        call(['mpc', 'play'])
        return "OK"

    # pause song
    def pause(self):
        call(['mpc', 'pause'])
        return "OK"

    # pause song
    def prev(self):
        call(['mpc', 'prev'])
        return "OK"

    # pause song
    def next(self):
        call(['mpc', 'next'])
        return "OK"

    # get the current song
    def current(self):
        return check_output(['mpc', 'current']).decode('utf-8')

    # get the play state
    def playing(self):
        lines = check_output(['mpc', 'status']).decode('utf-8').split('\n')
        if len(lines) > 2:
            return lines[1][lines[1].find('[') + 1: lines[1].find(']')]
        return 'stopped'

    # return playlist
    def playlist(self):
        lines = check_output(['mpc', 'playlist']).decode('utf-8').split('\n')
        current = check_output(['mpc', 'current']).decode('utf-8')

        return [{'name' : x, 'iscurrent' : (current[:-1] == x)} for x in lines if len(x) != 0]

    # list video directory
    def list(self, search):
        dir = DirectoryCrawl(self.path())
        return dir.results()

    # handle a post request
    def post(self, command, vals, get = []):
        # handle commands
        if command == 'add':
            return self.add(vals.get('target',None))
        elif command == 'play':
            return self.play()
        elif command == 'pause':
            return self.pause()
        elif command == 'prev':
            return self.prev()
        elif command == 'next':
            return self.next()
        elif command == 'clear':
            return self.clear()

        abort(404)

    # handle a get request
    def get(self, command, get = []):
        # handle commands
        if command == 'playlist':
            return jsonify(self.playlist())
        elif command == 'list':
            return jsonify(self.list(get.get('search', '')))
        elif command == 'status':
            return self.playing()

        # command not found
        abort(404)

    # render the module
    def render(self, get = [], template_args = {}):
        # render templater
        return render_template("musicplayer.html", **template_args)
