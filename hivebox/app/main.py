# app/main.py
import sys
from .version import print_version
   
def main():
    """Main function that prints version and exits"""
    print_version()
    sys.exit(0)
   
if __name__ == "__main__":
    main()