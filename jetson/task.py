# All task that may be done by Jetson which is requested by web server
class Task:
    INIT = "init"
    ADD_TIME = "add_time"
    CHANGE_TIME = "change_time"
    DELETE_TIME = "delete_time"
    GET_TIME_LIST = "get_time_list"
    CHANGE_ACTIVATE = "change_activate"
    RESET = "reset"
    SEND = "send"