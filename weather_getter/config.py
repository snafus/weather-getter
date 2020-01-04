import configparser

cf = configparser.ConfigParser()

def read_config(fname):
    """Read configuration from given file

    """
    global cf
    cf.read(fname)
    return cf
