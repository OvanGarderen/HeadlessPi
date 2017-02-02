from contextlib import contextmanager
from flask import render_template, jsonify, abort
from subprocess import call, check_output

from mpd import MPDClient

from utils import DirectoryCrawl
from plugin import Server

class MusicServer(Server):
    
    ### initialise the server
    def __init__(self, defaults, config):
        super().__init__(defaults, config)
        
        # connect to mpd server
        self._client = MPDClient()
        self._client.timeout = 10
        self._client.idletimeout = None

    ### settings
    def name(self):
        return self.option("mod-name", "Music Player")

    def icon(self):
        return self.option("mod-icon", "music")

    ### connection
    @contextmanager
    def connection(self):
        try:
            self._client.connect("localhost", int(self.option("mpd-port", 6600)))
            yield
        finally:
            self._client.close()
            self._client.disconnect()

    ### server commands

    # add song to the list
    def add(self, target):
        if target:
            print(target)
            self._client.add(target)
            return "OK"
        abort(404)
        
    # clear playlist
    def clear(self):
        self._client.clear()
        return "OK"

    # play song
    def play(self):
        self._client.play()
        return "OK"

    # pause song
    def pause(self):
        self._client.pause()
        return "OK"

    # pause song
    def prev(self):
        self._client.previous()
        return "OK"

    # pause song
    def next(self):
        self._client.next()
        return "OK"

    # get the current song
    def current(self):
        return self._client.currentsong()

    # get the play state
    def status(self):
        return self._client.status()

    # return playlist
    def playlist(self):
        return {"queue": self._client.playlistid(),
                "current": self._client.currentsong()}

    def playlist_remove(self, id):
        # remove song with id
        if id != None:
            self._client.deleteid(id)
            return "OK"

        # invalid id
        abort(500)

    # list video directory
    def list(self):
        ret = []
        
        # get a list of artists
        artists = self._client.list("albumartist")

        # get more info and combine artists
        for artist in artists:
            ret.append({"name" : artist})
        
        return ret

    def list_artist(self, artist):
        return self._client.list("album", "artist", artist)

    def list_album(self, artist, album):
        ret = []
        
        # get a list of song titles
        titles = self._client.list("title", "artist", artist, "album", album)
        
        # get more info
        for title in titles:
            if len(title) == 0:
                continue

            file = self._client.list("file", "artist", artist, "album", album, "title", title)
            track = self._client.list("track", "artist", artist, "album", album, "title", title)
            ret.append({"file" : file, "track" : track, "name" : title})
            
        # sort based on track number
        ret = sorted(ret, key = lambda x: x["track"])

        return ret

    # handle a post request
    def post(self, command, vals, get = []):
        
        # establish a connection to mpd
        with self.connection():
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
            elif command == 'playlist-remove':
                return self.playlist_remove(vals.get('id', None))

        abort(404)

    # handle a get request
    def get(self, command, get = []):

        # establish a connection to mpd
        with self.connection():
            print("Getting ", command)
            # handle commands
            if command == 'playlist':
                return jsonify(self.playlist())
            elif command == 'list':
                return jsonify(self.list())
            elif command == 'list_artist':
                return jsonify(self.list_artist(get.get("artist", "")))
            elif command == 'list_album':
                return jsonify(self.list_album(get.get("artist", ""), get.get("album", "")))
            elif command == 'status':
                return jsonify(self.status())

        # command not found
        abort(404)

    # render the module
    def render(self, get = [], template_args = {}):
        # render templater
        return render_template("musicplayer.html", **template_args)
