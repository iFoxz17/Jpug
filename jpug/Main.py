import sys
from view import UI

def main():
    args = sys.argv[1:]

    if len(args) == 0:
        ui = UI.UI()
        ui.start_ui()

    else:
        #TODO: Implement command line arguments
        pass

if __name__ == '__main__':
    main()