import curses
from windows import WindowManager



if __name__ == "__main__":

    def main(stdsrc):
        window_manager = WindowManager(stdsrc)
        window_manager.run()
    
    curses.wrapper(main)
    