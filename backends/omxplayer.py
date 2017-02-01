from omxplayer import OMXPlayer

import cec

class OMXPlayerBackend:
    def __init__(self, config):
        self._config = config

        self._player = None
        
    ### commands given with remote
    def remote(self, key, time):      
        # need a player for these commands
        if self._player == None:
            return
        
        if key == cec.CEC_USER_CONTROL_CODE_PLAY:
            self._player.play_pause()
        
        elif key == cec.CEC_USER_CONTROL_CODE_PAUSE:
            self._player.play_pause()
        
        elif key == cec.CEC_USER_CONTROL_CODE_STOP:
            self._player.quit()
        
        elif key == cec.CEC_USER_CONTROL_CODE_REWIND:
            self._player.set_position(self._player.position() - (time/10.0)*(time/10.0))
        
        elif key == cec.CEC_USER_CONTROL_CODE_FAST_FORWARD:
            self._player.set_position(self._player.position() + (time/10.0)*(time/10.0))
            

    ### commands
    def reset(self):
        # if we don't have a player there is nothing to do
        if self._player == None:
            return
        
        self._player.quit()
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
            self.reset()
            return 0
        
        if not self._player.position():
            self.reset()
            return 0

        # calculate position as percentage
        percentage = 100 * (float(self._player.position()) / self._player.duration())
        return percentage		


    def paused(self):
        if self._player == None:
            return True
        return not self._player.is_playing()

