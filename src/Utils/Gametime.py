
class GameTimeTracker:
    def __init__(self):
        self.in_game = False
        self._last_game_time = 0
        self._current_time = 0
        self._elapsed_time = 0
        self._temp_time = 0
        self._average_time = 0
        self._game_count = 0

    def start_tracking(self):
        """Start tracking"""
        self.in_game = True

    def stop_tracking(self):
        """Stop tracking"""
        self.in_game = False
        self._last_game_time = self._temp_time

    def get_last_game_time(self):
        """Getter for the last game time"""
        return self._last_game_time
    
    def update_time(self):
        """Update the ingame time counter"""
        if self.in_game:
            self._elapsed_time = self._elapsed_time + 1
            self._current_time = self._elapsed_time
            self._temp_time = self._current_time
        else:
            self._elapsed_time = 0

    def get_current_time(self):
        """Getter for current time"""
        return self._current_time
    
    def format_time(self, seconds):
        """Returns formatted time of format hh:mm:ss"""
        hours, remainder = divmod(seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        return f"{int(hours):02d}:{int(minutes):02d}:{int(seconds):02d}"
    
    def average_time(self):
        """Updates the average time and game count"""
        self._average_time += self._last_game_time
        self._game_count += 1

    def get_average_time(self):
        """Calculate the average time"""
        if self._game_count != 0:
            return self._average_time / self._game_count
        else:
            return self._average_time
    
    def get_game_count(self):
        """Getter for the game count"""
        return self._game_count