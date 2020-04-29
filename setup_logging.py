import logging
import sys
import os

def setup_logging(
    log_filepath = <fully_qualified_path_to_log_file>
    ,delete_previous_log = <True/False>
):

    # delete previous log file
    if os.path.exists(log_filepath) and delete_previous_log:
        os.remove(log_filepath)

    # create new class to assign to stderr and stdout
    class logger(object):
        def __init__(self):
            self.terminal = sys.stdout
            self.log = open(log_filepath, "w",encoding='utf-8')
            self.log.close()

        def write(self, message):
            self.terminal.write(message)
            self.log = open(log_filepath, "a",encoding='utf-8')
            self.log.write(message)  
            self.log.close()  

        def flush(self):
            pass

    return(logger)

