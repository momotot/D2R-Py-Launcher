
class GameTimeTracker:
    def __init__(self):
        self.in_game = False
        self.__last_game_time = 0
        self.__current_time = 0
        self.__elapsed_time = 0
        self.__temp_time = 0
        self.__average_time = 0
        self.__game_count = 0

    # start tracking
    def start_tracking(self):
        self.in_game = True

    # stop tracking
    def stop_tracking(self):
        self.in_game = False
        self.__last_game_time = self.__temp_time

    # getter for the last game time
    def get_last_game_time(self):
        return self.__last_game_time
    
    # update the ingame time counter
    def update_time(self):
        if self.in_game:
            self.__elapsed_time = self.__elapsed_time + 1
            self.__current_time = self.__elapsed_time
            self.__temp_time = self.__current_time
        else:
            self.__elapsed_time = 0

    # getter for current time
    def get_current_time(self):
        return self.__current_time
    
    # return formatted time of format hh:mm:ss
    def format_time(self, seconds):
        hours, remainder = divmod(seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        return f"{int(hours):02d}:{int(minutes):02d}:{int(seconds):02d}"
    
    # update the average time and game count
    def average_time(self):
        self.__average_time += self.__last_game_time
        self.__game_count += 1

    # calculate the average time
    def get_average_time(self):
        if self.__game_count != 0:
            return self.__average_time / self.__game_count
        else:
            return self.__average_time
    
    # getter for the game count
    def get_game_count(self):
        return self.__game_count