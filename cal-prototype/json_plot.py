import sys

import json
from pprint import pprint

import time #for sleep
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

import os #for getext()

def getext(filename):
    return os.path.splitext(filename)[-1].lower()

class ChangeHandler(FileSystemEventHandler):

    """
    event.event_type 
        'modified' | 'created' | 'moved' | 'deleted'
    event.is_directory
        True | False
    event.src_path
        path/to/observed/file
    """

    def on_modified(self, event):
        if getext(event.src_path) == '.json':
            print "modify" 

    def on_created(self, event):
        if getext(event.src_path) == '.json':
            print "create"


if __name__ == '__main__':
    event_handler = ChangeHandler()
    observer = Observer()
    observer.schedule(event_handler, '.')
    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()

    observer.join()



#json_data = open('output.json');

#data = json.load(json_data);
#pprint(data);

#json_data.close();

#print data["PAR"] 
