import time

from logger import Logger


class Timer:
    """
    Time setting
    """

    ADD_TIME = "add_time"
    CHANGE_TIME = "change_time"
    DELETE_TIME = "delete_time"
    GET_TIME_LIST = "get_time_list"

    def __init__(self, logger: Logger) -> None:
        self.timelist = []
        self.logger = logger

    def add_time(self, t: time.struct_time) -> bool:
        """
        Add time to current time list

        t: time to add
        """
        self.timelist.append(t)
        self.timelist = sorted(self.timelist)
        add_t = time.strftime("%H:%M:%S", t)
        self.logger.success(f"Add time {add_t}")
        return True

    def change_time(self, source_time: time.struct_time, target_time: time.struct_time) -> bool:
        """
        Change time in current time list

        source_time: time to change to
        target_time: time begin modified
        """
        target_t = time.strftime("%H:%M:%S", target_time)
        if target_time not in self.timelist:
            self.logger.error(f"Time {target_t} isn't in current list")
            self.logger.info(f"Current time list:")
            for t in self.timelist:
                self.logger.info(time.strftime("%H:%M:%S", t))
            return False

        idx = self.timelist.index(target_t)
        self.timelist[idx] = source_time
        self.timelist = sorted(self.timelist)
        source_t = time.strftime("%H:%M:%S", source_time)
        self.logger.success(f"Change time {target_t} to {source_t}")
        return True

    def delete_time(self, t: time.struct_time) -> bool:
        """
        Delete time from current time list

        t: time to delete
        """
        delete_t = time.strftime("%H:%M:%S", t)
        if t not in self.timelist:
            self.logger.error(f"Time {delete_t} isn't in current list")
            self.logger.info(f"Current time list:")
            for t in self.timelist:
                self.logger.info(time.strftime("%H:%M:%S", t))
            return False

        self.timelist.remove(t)
        self.logger.success(f"Delete time {delete_t}")
        return True

    def get_time(self) -> time.struct_time:
        """
        Get the nearest future time, use binary search
        """

    def get_all(self) -> list:
        """
        Get the whole time list
        """
        self.logger.success("Get whole timelist")
        return self.timelist.copy()
