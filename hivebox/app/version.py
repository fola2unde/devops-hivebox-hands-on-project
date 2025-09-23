# app/version.py
__version__ = "0.0.1"
   
def get_version():
    return __version__
   
def print_version():
    print(f"HiveBox version: {get_version()}")
    return get_version()