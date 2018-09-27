#coding: utf-8

import ast

def readDict(filename):
    try:
        r = open(filename, "r")
        db_data = r.read()
        if db_data == "" or db_data is None:
            db_data = "{}"

        dict = ast.literal_eval(db_data)
        r.close()

        return dict
    except BaseException:
        print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
        print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
        print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
        print("FileUtils: Unable to load " + filename)
        print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
        print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
        print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
        return {}

def saveDict(map, filename):
    cleanFile(filename)
    a = open(filename, "a")
    a.write(str(map))
    a.flush()
    a.close()


def cleanFile(filename):
    open(filename, "w").close()
