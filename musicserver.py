from flask import render_template, jsonify, abort
from subprocess import call, check_output

class MusicServer:
    def name(self):
        return "Music Player"

    def icon(self):
        return "music"

    # add song to the list
    def add(target):
        print(target)
        if len(target) > 0:
            call(['mpc', 'add', target])

    # clear playlist
    def clear():
        call(['mpc', 'clear'])

    # play song
    def play():
        call(['mpc', 'play'])

    # pause song
    def pause():
        call(['mpc', 'pause'])

    # pause song
    def prev():
        call(['mpc', 'prev'])

    # pause song
    def next():
        call(['mpc', 'next'])

    # get the current song
    def current():
        return check_output(['mpc', 'current']).decode('utf-8')

    # get the play state
    def playing():
        lines = check_output(['mpc', 'status']).decode('utf-8').split('\n')
        if len(lines) > 2:
            return lines[1][lines[1].find('[') + 1: lines[1].find(']')]
        return 'stopped'

    # return playlist
    def playlist():
        lines = check_output(['mpc', 'playlist']).decode('utf-8').split('\n')
        current = check_output(['mpc', 'current']).decode('utf-8')

        return [{'name' : x, 'iscurrent' : (current[:-1] == x)} for x in lines if len(x) != 0]

    # handle a post request
    def post(self, command, vals, get = []):        
        # handle commands
        if command == 'add':
            MusicServer.add(vals.get('target',''))
        elif command == 'play':
            MusicServer.play()
        elif command == 'pause':
            MusicServer.pause()
        elif command == 'prev':
            MusicServer.prev()
        elif command == 'next':
            MusicServer.next()
        elif command == 'clear':
            MusicServer.clear()

        return "OK"

    # handle a get request
    def get(self, command, get = []):
        # handle commands
        if command == 'playlist':
            return jsonify(MusicServer.playlist())
        elif command == 'status':
            return MusicServer.playing()

        # command not found
        abort(404)

    # render the module
    def render(self, get = [], template_args = {}):
        # render templater
        return render_template("musicplayer.html", **template_args)
