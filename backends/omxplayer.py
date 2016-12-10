from omxplayer import OMXPlayer

class OMXPlayerBackend:
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
                
        # delete the player
        del self._player

        # set the player to empty
        self._player = None

    def start(self, target):
        # reset the player
        self.reset()
        
        # start the player
        self._player = OMXPlayer(target)
        
    def pause(self):
        # if we don't have a player there is nothing to do
        if self._player == None:
            return

        # toggle the pause state
        self._player.play_pause()

    def seek(self, value):
        # if we don't have a player there is nothing to do
        if self._player == None:
            return
        
        # convert to float
        value = float (value)
     
        # constrain value
        if value > 100:
            value = 100
        elif value < 0:
            value = 0

        # get the duration
        duration = self._player.duration()

        # seek to position, in seconds
        self._player.set_position((value/100) * duration)

    ### get values
    def position(self):
        # if we don't have a player there is nothing to do
        if self._player == None:
            return 0        

        # check that we dont divide by zero
        if self._player.duration() == 0:
            return 0

        # calculate position as percentage
        percentage = 100 * (float(self._player.position()) / self._player.duration())
        print(percentage)       
        return percentage		


    def paused(self):
        if self._player == None:
            return False
        return not self._player.is_playing()

