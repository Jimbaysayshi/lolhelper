import tkinter as tk
import pyautogui
import time
import pyperclip
import win32gui
import pywinauto
import json
from selenium import webdriver
from pywinauto.timings import TimeoutError
from pywinauto.application import Application
from selenium.common.exceptions import WebDriverException, NoSuchWindowException, ElementClickInterceptedException

choose_champ = ['choosechamp.PNG', 'banphase.png']
messages = {'add': 'Start by adding a summoner \n',
            'start': 'Seems like League of legends is not active, start it and try again \n',
            'not': 'Not in championselect, try again \n'}


class SearchHelper(object):

    def type_keys(self, summoners):
        """Find handle for lolhelper and automatically type summoner names to textfield """
        self.clear_field()
        app = Application()
        window_handle = pywinauto.findwindows.find_windows(title='LoLstats')
        app.connect(handle=window_handle[0])
        app_dialog = app.window(title_re="LoLstats")

        app_dialog.set_focus()
        # app.LoLstats.draw_outline("red")
        for summoner in summoners:
            if ':' in summoner:
                continue
            else:
                self.textfield.insert(tk.INSERT, summoner)  # INSERT OR END?
        time.sleep(len(summoners))

    def is_champselect(self, window_pos):
        """Check if user is in championselection, pyautogui.locateOnScreen uses relative position of league of legends window"""
        for pic in choose_champ:
            select = pyautogui.locateOnScreen(
                pic, region=window_pos)
        if select == None:
            return False
        return True

    def copy_summoners(self):
        """With Lol handler get position of th window and automatically copy summoner names from championselection"""
        hwnd = pywinauto.findwindows.find_windows(
            title='League of Legends')
        try:
            pos = win32gui.GetWindowRect(hwnd[0])
        except IndexError:
            msg = messages['start']
            self.textfield.insert(tk.INSERT, msg)
            return
        win32gui.SetForegroundWindow(hwnd[0])
        tries = 5
        tried = 0
        while self.is_champselect(pos) != True:
            if tried >= tries:
                self.write_to_field(messages['not'])
                self.champselect = False
                return None
            tried += 1
            time.sleep(0.5)
        self.champselect = True
        # pyautogui needs 0.2 seconds to move mouse and user cant move at the time? TODO any other way?
        pyautogui.moveTo(pos[0]+240, pos[3]-50)
        pyautogui.dragTo(pos[0]+25, pos[3]-180)
        pyautogui.hotkey('ctrl', 'c')
        time.sleep(.01)
        # paste summoners from clipboard to an array
        summoners = [pyperclip.paste()]

        return self.type_keys(summoners)

    def get_browser(self):
        """Get browser from settings['path'] and correct settings for the browser"""
        self.browser = webdriver.Chrome(
            self.settings['chromepath'], options=self.chrome_options)
        self.browser.get(self.site)
        try:
            cookie_policy = self.browser.find_element_by_xpath(
                '/html/body/div[4]/div[1]/div/div/div[4]/button[2]')
            cookie_policy.click()
        except (AttributeError, ElementClickInterceptedException):
            pass

    def continue_in_browser(self):
        self.browser.get(self.site)

    def search_summoners(self, text):
        """Find correct textfield from the site and automatcially focus on it, valid summoners and start search"""
        try:
            search_field = self.browser.find_element_by_xpath(
                '/html/body/div[2]/div[2]/div[2]/div/div[1]/div[1]/form/textarea')
            search_btn = self.browser.find_element_by_xpath(
                '/html/body/div[2]/div[2]/div[2]/div/div[1]/div[1]/form/button')
        except WebDriverException:

            return self.start_search()
        search_field.click()
        search_field.clear()
        search_field.send_keys(text)
        time.sleep(1)
        search_btn.click()

    def start_search(self):
        """validate textfield and define if new browser is needed"""
        # TODO breaks if browser is closed?

        text = self.get_field_msg()
        if text == None or text in messages.values():
            return
        if self.searches != 0:
            self.continue_in_browser()
        else:
            self.get_browser()
        self.searches += 1
        self.search_summoners(text)

    def automatic_search(self):
        self.clear_field()
        self.copy_summoners()
        if self.champselect == True:
            self.start_search()

    def clear_field(self):
        # Helper to clear textfield
        self.textfield.delete('1.0', tk.END)

    def write_to_field(self, msg):
        # Helper to write to textfield
        self.textfield.insert(tk.INSERT, msg)

    def get_field_msg(self):
        # Helper to get textfield message and low level validation
        text = self.textfield.get("1.0", 'end-1c')
        if text == "":
            self.write_to_field(messages['add'])
            return None
        else:
            return text

    def __init__(self, settings):
        self.settings = settings
        self.champselect = False
        self.searches = 0
        self.site = f"https://{self.settings['region']}{self.settings['op']}"
        # selenium
        self.chrome_options = webdriver.ChromeOptions()
        prefs = {"profile.default_content_settings_values.notifications": 2}
        self.chrome_options.add_experimental_option("prefs", prefs)
        # self.arguments = ["--ignore-certificate-errors",
        #                  "--disable-popup-blocking", "--incognito"]
        for args in self.settings['chrome_args']:
            self.chrome_options.add_argument(args)

        # Create tkinter window
        self.root = tk.Tk()
        self.root.resizable(width=False, height=False)
        self.textfield = tk.Text(self.root, height=10, width=40)
        self.start_btn = tk.Button(
            self.root, command=self.start_search, text='Start Search')
        self.automatic_btn = tk.Button(
            self.root, command=self.automatic_search, text='Automatic Search')
        self.clear_btn = tk.Button(
            self.root, command=self.clear_field, text='Clear Fields')

        # Title
        self.root.title('LoLstats')

        # button grids
        self.textfield.grid(row=0, columnspan=3)
        self.clear_btn.grid(row=1, column=2, sticky='E')
        self.start_btn.grid(row=1, column=1)
        self.automatic_btn.grid(row=1, column=0, sticky='W')

        # start tkinter loop
        self.root.mainloop()
