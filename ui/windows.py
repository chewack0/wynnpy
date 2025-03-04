from typing import List

from abc import ABC, abstractmethod
import curses
import os

class WindowManager:

    #windows = {"WindowName":window_instance, ...}
    #
    #
    def __init__(self, stdscr):
        self.stdscr = stdscr
        self.windows = {"Main Menu": MainMenu("Main Menu", self.stdscr, self),
                        "Test": TestWindow("Test", self.stdscr, self)}
        self.active = self.windows.get("Main Menu", TestWindow("Test", self.stdscr, self))
        self.mix_y = 30
        self.min_x = 60
        self.calculate_size()

    def switch_window(self, name):
        self.active = self.windows.get(name, TestWindow("Test", self.stdscr, self))

    def calculate_size(self):
        self.max_y, self.max_x = self.stdscr.getmaxyx()
        self.max_y = self.max_y - 1 
        self.max_x = self.max_x - 2
        self.center_y = self.max_y // 2
        self.center_x = self.max_x // 2 
            
    def handle_input(self, c):
        if c == curses.KEY_RESIZE:
            self.calculate_size()
        elif c == curses.KEY_UP:
            self.active.cursor[0] = (self.active.cursor[0] - 1) % len(self.active.items)
        elif c == curses.KEY_DOWN:
            self.active.cursor[0] = (self.active.cursor[0] + 1) % len(self.active.items)
        elif c == curses.KEY_LEFT:
            self.active.cursor[1] = (self.active.cursor[1] - 1) % len(self.active.items[self.active.cursor[0]])
        elif c == curses.KEY_RIGHT:
            self.active.cursor[1] = (self.active.cursor[1] + 1) % len(self.active.items[self.active.cursor[0]])
        elif c == curses.KEY_ENTER or c in [10, 13]:  # Handle Enter key
            self.active.handle_enter()
        elif c == ord(":"): #There I wannd make some vim type commands
            self.handle_command_line()
            return False
        return True

    def update_display(self):
        if self.max_y < self.mix_y or self.max_x < self.min_x:
            self.stdscr.addstr(0, 0, f"TERMINAL WINDOW IS TOO SMALL")
        self.active.update_display()
        self.status_bar()

    def status_bar(self):
        for i in range(self.max_x):
            self.stdscr.addch(self.max_y, i, " ", curses.A_REVERSE)
        self.stdscr.addstr(self.max_y, self.center_x - len(self.active.name)//2, self.active.name, curses.A_REVERSE)

    def run(self):
        self.active.update_display()
        while True:
            curses.curs_set(0)
            c = self.stdscr.getch()
            self.handle_input(c)
            self.update_display()
            if c == ord("q"):  # 'q' key duh
                break
    
    

class Window(ABC):

    def __init__(self, name: str, stdscr, window_manager, *args, **kwargs):

        if isinstance(window_manager, WindowManager):
            self.wm = window_manager
        else:
            raise TypeError(f"Expected to recieve WindowManager instance")
        
        self.name = name
        self.stdscr = stdscr
        self.cursor = [0, 0] #y, x item under the cursor
        #self.minimumTerminalSize = [60, 30]




    def handle_command_line(self):
        pass
    
    @abstractmethod
    def handle_enter(self):
        pass
    
    def update_display(self):
        self.stdscr.clear()


    
    def add_debug_marks(self):
        self.stdscr.addch(0, 0, "x", curses.color_pair(3))
        self.stdscr.addstr(1, 1, f"(0, 0)")
        self.stdscr.addch(0, self.wm.max_x, "x", curses.color_pair(3))
        self.stdscr.addstr(1, self.wm.max_x - len(f"(0, {self.wm.max_x})"), f"(0, {self.wm.max_x})")
        self.stdscr.addch(self.wm.max_y, 0, "x", curses.color_pair(3))
        self.stdscr.addstr(self.wm.max_y - 1, 1, f"({self.wm.max_y}, 0)")
        self.stdscr.addch(self.wm.max_y, self.wm.max_x, "x", curses.color_pair(3))
        self.stdscr.addstr(self.wm.max_y - 1, self.wm.max_x - len(f"({self.wm.max_y}, {self.wm.max_x})"), f"({self.wm.max_y}, {self.wm.max_x})")
        self.stdscr.addch(self.wm.center_y, self.wm.center_x, "x", curses.color_pair(3))
        self.stdscr.addstr(self.wm.center_y + 1, self.wm.center_x + 1, f"({self.wm.center_y}, {self.wm.center_x})")



class TestWindow(Window):


    def __init__(self, name, stdscr, *args, **kwargs):
        super().__init__(name, stdscr, *args, **kwargs)
        self.items = [["ITEM0", "ITEM1", "ITEM2"]]
        self.color = 0

    def handle_enter(self):
        self.wm.switch_window("Main Menu")

    def update_display(self):
        super().update_display()
    
        if self.wm.max_y < self.wm.mix_y or self.wm.max_x < self.wm.min_x:
            self.stdscr.addstr(0, 0, f"TERMINAL WINDOW IS TOO SMALL")
        else:
            self.add_debug_marks()

        self.stdscr.refresh()

class MainMenu(Window):

    def __init__(self, name, stdscr, *args, **kwargs):
        super().__init__(name, stdscr, *args, **kwargs)
        self.items = [{"ITEM0": self.func0, "ITEM1": self.func1, "ITEM2": self.func2}]

        self.content = " "
        curses.start_color()
        curses.init_pair(1, curses.COLOR_RED, curses.COLOR_BLACK)    
        curses.init_pair(2, curses.COLOR_GREEN, curses.COLOR_BLACK)  
        curses.init_pair(3, curses.COLOR_BLUE, curses.COLOR_BLACK)  
        self.color = curses.color_pair(1)

    def func0(self):
        self.color = 0 # Update display to reflect changes
        self.content = "FUNCTION 0 EXECUTED (buttons white)"

    def func1(self):
        self.wm.switch_window("Test")

    def func2(self):
        self.color = 3
        self.content = "FUNCTION 2 EXECUTED (buttons blue)"
    

    def handle_enter(self):
        self.items[0][self.selected]()


    def update_display(self):
        super().update_display()       
        self.stdscr.addstr(self.wm.center_y - 4, self.wm.center_x - len(self.content)//2, self.content)

        
        for i, row in enumerate(self.items):
            for j, col in enumerate(row):
                content_len = len(col)
            
                if self.cursor[0] == i and self.cursor[1] == j:
                    self.selected = col
                    self.stdscr.addstr(self.wm.center_y, self.wm.center_x - (content_len+4) + j*(len(col)+2), col, curses.A_REVERSE)
                else:
                    self.stdscr.addstr(self.wm.center_y, self.wm.center_x - (content_len+4) + j*(len(col)+2), col, curses.color_pair(self.color))

        self.add_debug_marks()