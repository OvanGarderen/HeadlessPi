from flask import render_template, jsonify, abort
from subprocess import call, check_output
from pathlib import Path

class DirectoryCrawl:
    def __init__(self, base, search = ''):
        self._path = Path(base)
        self._results = self.read_dir(self._path)
        self._results['name'] = '/'

    def read_dir(self, path):
        # recurse
        children = [self.read_dir(x) for x in path.iterdir()] if path.is_dir() else None

        # make dictionary
        return {'path' : path.relative_to(self._path).as_posix(), 'name' : path.parts[-1], 'isdir' : path.is_dir(), 'children' : children}
        
    def results(self):
        print(self._results)
        return self._results

class VideoServer:
    def name(self):
        return "Video Player"

    def icon(self):
        return "play-circle-o"

    def videopath(self):
        return "/home/okke/Visuals"

    # add song to the list
    def play(self, target):
        if call(['mpv', self.videopath() + '/' + target]) != 0:
            abort(404)

    # get the local path for a video
    def play_local(self, target):
        call(['ln', '-s', self.videopath() + '/' + target, 'resources/tmp/' + target])

        return '/resources/tmp/' + target

    # list video directory
    def list(self, search):
        return DirectoryCrawl(self.videopath()).results()

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
