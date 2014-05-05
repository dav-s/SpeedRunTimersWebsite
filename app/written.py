from datetime import datetime
import os

def write_message(name, email, title, content):
    path = "generated/messages/"
    if not os.path.exists(path):
        os.makedirs(path)
    fname = "%s - %s.txt" % (title, datetime.now().day)
    f = open(os.path.join(path, fname), "w+")
    f.write("%s, %s\n%s" % (name, email, content))
    f.close()

