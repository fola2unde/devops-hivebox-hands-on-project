# app/main.py
import sys
import argparse
from .version import print_version
from .api import create_app

def main():
    """Main function with argument parsing"""
    parser = argparse.ArgumentParser(description='HiveBox API')
    parser.add_argument('--version', action='store_true', 
                       help='Print version and exit')
    parser.add_argument('--serve', action='store_true',
                       help='Start API server')
    
    args = parser.parse_args()
    
    if args.version:
        print_version()
        sys.exit(0)
    elif args.serve:
        app = create_app()
        app.run(debug=True, host='0.0.0.0', port=5000)
    else:
        # Default behavior: print version and exit
        print_version()
        sys.exit(0)

if __name__ == "__main__":
    main()