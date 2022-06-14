from logger import Logger


def tstr2int(tstr: str) -> int:
    """
    tstr: format like 07:23, 21:54
    """
    t = tstr.split(":")
    return int(t[0]) * 60 + int(t[1])


class Timer:
    """
    Time setting
    """

    ADD_TIME = "add_time"
    CHANGE_TIME = "change_time"
    DELETE_TIME = "delete_time"
    CHANGE_ACTIVATE = "change_activate"
    GET_TIME_LIST = "get_time_list"

    def __init__(self, logger: Logger) -> None:
        """
        time item format
        {
            time: hh:mm,
            activate: True/False
        }
        """
        self.timelist = []
        self.logger = logger

    def add_time(self, time: str) -> bool:
        """
        Add time to current time list

        time: time to add
        """
        time = time.zfill(5)
        _list = [x["time"] for x in self.timelist]

        if time in _list:
            self.logger.error(f"Time {t} already in current list")
            self.logger.info(f"Current time list:")
            for t in self.timelist:
                info = t["time"] + ", activate: %b" % t["activate"]
                self.logger.info(info)
            return False

        self.timelist.append({"time": time, "activate": True})
        self.timelist = sorted(self.timelist, key=lambda x: tstr2int(x["time"]))
        self.logger.success(f"Add time {time}")
        return True

    def change_time(self, source_time: str, target_time: str) -> bool:
        """
        Change time in current time list

        source_time: time to change to
        target_time: time begin modified
        """
        source_time = source_time.zfill(5)
        target_time = target_time.zfill(5)
        _list = [x["time"] for x in self.timelist]

        if target_time not in _list:
            self.logger.error(f"Time {target_time} isn't in current list")
            self.logger.info(f"Current time list:")
            for t in self.timelist:
                info = t["time"] + ", activate: %b" % t["activate"]
                self.logger.info(info)
            return False

        idx = _list.index(target_time)
        self.timelist[idx]["time"] = source_time
        self.timelist = sorted(self.timelist, key=lambda x: tstr2int(x["time"]))
        self.logger.success(f"Change time {target_time} to {source_time}")
        return True

    def delete_time(self, time: str) -> bool:
        """
        Delete time from current time list

        time: time to delete
        """
        time = time.zfill(5)
        _list = [x["time"] for x in self.timelist]

        if time not in _list:
            self.logger.error(f"Time {time} isn't in current list")
            self.logger.info(f"Current time list:")
            for t in self.timelist:
                info = t["time"] + ", activate: %b" % t["activate"]
                self.logger.info(info)
            return False

        for i in range(len(self.timelist)):
            if self.timelist[i]["time"] == time:
                del self.timelist[i]
                break
        self.logger.success(f"Delete time {time}")
        return True

    def change_activate(self, time: str) -> bool:
        """
        Change specified time activate status

        time: time to change
        """
        time = time.zfill(5)
        _list = [x["time"] for x in self.timelist]

        if time not in _list:
            self.logger.error(f"Time {time} isn't in current list")
            self.logger.info(f"Current time list:")
            for t in self.timelist:
                info = t["time"] + ", activate: %b" % t["activate"]
                self.logger.info(info)
            return False

        result = None
        for i in range(len(self.timelist)):
            if self.timelist[i]["time"] == time:
                self.timelist[i]["activate"] ^= True
                result = self.timelist[i]["activate"]
                break
        self.logger.success(f"Change time {time} activate to {result}")
        return True

    def get_all(self) -> list:
        """
        Get the whole time list
        """
        self.logger.success("Get whole timelist")
        return self.timelist.copy()
