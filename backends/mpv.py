from jaseg.mpv import MPV

class MPVBackend:
    def __init__(self, config):
        self._config = config

        self._player = None

    ### commands
    def reset(self):
        # if we don't have a player there is nothing to do
        if self._player == None:
            return
        
        # send the quit command
        self._player.quit()
        
        # wait for the player to quit
        self._player.wait_for_playback()
        
        # delete the player
        del self._player

        # set the player to empty
        self._player = None

    def start(self, target):
        # reset the player
        self.reset()
        
        # start the player
        self._player = MPV()
        
        # play the file
        self._player.play(target)

        print(self._player, target)
        
    def pause(self):
        # if we don't have a player there is nothing to do
        if self._player == None:
            return

        # toggle the pause state
        self._player.pause = not self._player.pause

    def seek(self, value):
        # if we don't have a player there is nothing to do
        if self._player == None:
            return
        
        value = float(value)

        if value > 100:
            value = 100
        elif value < 0:
            value = 0

        print(value)

        # seek to position
        self._player.seek(value, reference="absolute-percent")

    ### get values
    def position(self):
        if self._player == None:
            return 0        
        return self._player.percent_pos

    def paused(self):
        if self._player == None:
            return False
        return self._player.pause
