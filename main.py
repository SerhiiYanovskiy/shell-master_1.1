import re
import csv
import time
import pandas as pd
import PySimpleGUI as sg
from random import choice as ch

from random import randint as rd, random

import pandas.errors
from fake_useragent import UserAgent

from threading import Thread
from multiprocessing import Process

from seleniumwire import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains

likes_counter = 0
follows_counter = 0
comments_counter = 0
mixer_accounts = 0
mixer_follows = 0
login_comments = []
login_likes = []
user_agents = []
proxys = []
def new_data_comments():

    with open("comments/logins, passwords.csv", "r") as f:
        nums = f.read().splitlines()
        for elem in nums:
            if elem != "login,password":
                login_comments.append(elem)
            else:
                continue

    with open("user_agents.csv", "r") as f:
        nums = f.read().splitlines()
        for elem in nums:
            user_agents.append(elem)

    with open("proxy_export.csv", "r") as f:
        nums = f.read().splitlines()
        for elem in nums:
            proxys.append(elem)

    with open("comments/all_data_about_accounts.csv", "w") as file:
        file.write("login,password,user_agent,proxy_port,proxy_ip,proxy_login,proxy_password\n")

    with open("comments/all_data_about_accounts.csv", "a") as file:
        for elem in login_comments:
            file.write(f"{elem},{ch(user_agents)},{ch(proxys)}\n")


def new_data_liks():

    with open("likes, followers/logins, passwords.csv", "r") as f:
        nums = f.read().splitlines()
        for elem in nums:
            if elem != "login,password":
                login_likes.append(elem)
            else:
                continue




    with open("likes, followers/all_data_about_accounts.csv", "a") as file:
        for elem in login_likes:
            file.write(f"{elem},{ch(user_agents)},{ch(proxys)}\n")
    time.sleep(3)





def main():
    new_data_comments()
    new_data_liks()
    layout = [
        [sg.Button('Likes', key='Likes', ), sg.Button('Followers', key='Followers'),
         sg.Button('Comments', key='Comments'), sg.Button('Mixer', key='Mixer')]
    ]
    window = sg.Window('Choose', layout, element_justification = "c")
    while True:
        events, values = window.read()
        if events == sg.WIN_CLOSED:
            return

        if events == 'Likes':
            likes()
        elif events == 'Followers':
            followers()
        elif events == 'Comments':
            comments()
        elif events == 'Mixer':
            mixer()

def get_accounts(type_of: str):
    pd.options.display.max_colwidth = 999
    users = {}

    while True:
        try:
            data = pd.read_csv('%s/all_data_about_accounts.csv' % type_of)
            a = str(data.login).split('\n'); a.pop(-1)
            b = str(data.password).split('\n'); b.pop(-1)
            c = str(data.user_agent).split('\n'); c.pop(-1)
            logins = []
            passwords = []
            user_agents = []
            for i in range(len(a)):
                logins.append(re.findall(".\s(.+)", a[i])[0].strip())
                passwords.append(re.findall(".\s(.+)", b[i])[0].strip())
                user_agents.append(re.findall(".\s(.+)", c[i])[0].strip())
            try:
                d = str(data.proxy_ip).split('\n'); d.pop(-1)
                e = str(data.proxy_login).split('\n'); e.pop(-1)
                f = str(data.proxy_password).split('\n'); f.pop(-1)
                g = str(data.proxy_port).split('\n'); g.pop(-1)

                proxy = {}

                for i in range(len(a)):
                    proxy_ip = re.findall(".\s(.+)", d[i])[0].strip()
                    proxy_login = re.findall(".\s(.+)", e[i])[0].strip()
                    proxy_password = re.findall(".\s(.+)", f[i])[0].strip()
                    proxy_port = re.findall(".\s(.+)", g[i])[0].strip()
                    proxy[f"{proxy_ip}:{proxy_port}_{i}"] = {
                        "login": proxy_login,
                        "password": proxy_password
                    }

                items = []
                for k, v in proxy.items():
                    items.append([k, v["login"], v["password"]])

                for counter in range(len(items)):
                    users[logins[counter]] = {
                        "password": passwords[counter],
                        "user_agent": user_agents[counter],
                        "proxy": items[counter]
                    }
                # for i in range(len(logins)):
                #     users[logins[i]] = {
                #         "password": passwords[i],
                #         "user_agent": user_agents[i],
                #         "proxy": proxy[i]
                #     }
                return users, True
            except AttributeError:
                for counter in range(len(logins)):
                    users[logins[counter]] = {
                        "password": passwords[counter],
                        "user_agent": user_agents[counter]
                    }
                return users, False

        except:
            data = pd.read_csv('%s/logins, passwords.csv' % type_of)
            a = str(data.login).split('\n'); a.pop(-1)
            b = str(data.password).split('\n'); b.pop(-1)

            logins = []
            passwords = []
            for i in range(len(a)):
                logins.append(re.findall(".\s(.+)", a[i])[0].strip())
                passwords.append(re.findall(".\s(.+)", b[i])[0].strip())
            try:
                data = pd.read_csv('proxy_export.csv')
                c = str(data.proxy_ip).split('\n'); c.pop(-1)
                d = str(data.proxy_login).split('\n'); d.pop(-1)
                e = str(data.proxy_password).split('\n'); e.pop(-1)
                f = str(data.proxy_port).split('\n'); f.pop(-1)

                proxy = {}

                for i in range(len(c)):
                    proxy_ip = re.findall(".\s(.+)", c[i])[0].strip()
                    proxy_login = re.findall(".\s(.+)", d[i])[0].strip()
                    proxy_password = re.findall(".\s(.+)", e[i])[0].strip()
                    proxy_port = re.findall(".\s(.+)", f[i])[0].strip()
                    proxy[proxy_ip] = {
                        "login": proxy_login,
                        "password": proxy_password,
                        "port": proxy_port
                    }

                header = ['login', 'password', 'user_agent', 'proxy_port', 'proxy_ip', 'proxy_login', 'proxy_password']
                columns = []
                ua = UserAgent()
                ua.update()
                counter = 0
                for k, v in proxy.items():
                    for i in range(rd(2, 3)):
                        try:
                            user_agent = ua.random
                            columns.append([logins[counter], passwords[counter], user_agent, v["port"], k, v["login"], v["password"]])
                            counter += 1
                        except:
                            continue

                with open('%s/all_data_about_accounts.csv' % type_of, 'w', newline='') as csv_file:
                    csvwriter = csv.writer(csv_file)
                    csvwriter.writerow(header)
                    csvwriter.writerows(columns)
            except pandas.errors.EmptyDataError:
                header = ['login', 'password', 'user_agent']
                columns = []
                ua = UserAgent()
                ua.update()
                counter = 0
                for i in range(len(logins)):
                    user_agent = ua.random
                    columns.append([logins[counter], passwords[counter], user_agent])
                    counter += 1

                with open('%s/all_data_about_accounts.csv' % type_of, 'w', newline='') as csv_file:
                    csvwriter = csv.writer(csv_file)
                    csvwriter.writerow(header)
                    csvwriter.writerows(columns)

def likes():
    layout = [
        [sg.Text('Post URL')],
        [sg.InputText(key="link", size=(50, 1))],
        [sg.Text(' ')],
        [sg.Text('Number of likes'), sg.InputText(key='value', size=(5, 1))],
        [sg.Checkbox('Headless', default=True, key='checkbox')],
        [sg.Button('Start', key='Start')]
    ]
    window = sg.Window('Likes', layout, element_justification = "c")
    while True:
        events, values = window.read()
        if events == sg.WIN_CLOSED:
            return

        if events == 'Start':
            if values["value"].isdigit and values["link"] != '':
                value = int(values["value"])
                if value > 0:
                    th_likes = Process(target = start_likes, args = (values["link"], value, values["checkbox"]))
                    th_likes.start()

def followers():
    layout = [
        [sg.Text('Profile URL')],
        [sg.InputText(key="link", size=(50, 1))],
        [sg.Text(' ')],
        [sg.Text('Number of followers'), sg.InputText(key='value', size = (5, 1))],
        [sg.Checkbox('Headless', default=True, key='checkbox')],
        [sg.Button('Start', key='Start')]
    ]
    window = sg.Window('Followers', layout, element_justification = "c")
    while True:
        events, values = window.read()
        if events == sg.WIN_CLOSED:
            return

        if events == 'Start':
            if values["value"].isdigit and values["link"] != '':
                value = int(values["value"])
                if value > 0:
                    th_likes = Process(target=start_follows, args=(values["link"], value, values["checkbox"]))
                    th_likes.start()

def comments():
    layout = [
        [sg.Text('Post URL')],
        [sg.InputText(key = 'link', size = (50, 1))],
        [sg.Text(' ')],
        [sg.Text('Number of comments'), sg.InputText(key='value', size = (5, 1))],
        [sg.Checkbox('Headless', default = True, key = 'checkbox')],
        [sg.Button('Start', key = 'Start')]
    ]
    window = sg.Window('Comments', layout, element_justification = 'c')
    while True:
        events, values = window.read()
        if events == sg.WIN_CLOSED:
            return

        if events == 'Start':
            if values["value"].isdigit and values["link"] != '':
                value = int(values["value"])
                if value > 0:
                    th_likes = Process(target=start_comments, args=(values["link"], value, values["checkbox"]))
                    th_likes.start()

def mixer():
    layout = [
        [sg.Text('Followers for each account'), sg.InputText(key = 'followers', size = (5, 1))],
        [sg.Text('Accounts'), sg.InputText(key='accounts', size = (5, 1))],
        [sg.Checkbox('Headless', default = True, key = 'checkbox')],
        [sg.Button('Start', key = 'Start')]
    ]
    window = sg.Window('Mixer', layout, element_justification = 'c')
    while True:
        events, values = window.read()
        if events == sg.WIN_CLOSED:
            return

        if events == 'Start':
            if values["accounts"].isdigit and values["followers"].isdigit:
                accounts = int(values["accounts"])
                follows = int(values["followers"])
                if accounts > 0 and follows > 0:
                    th_mixer = Process(target=start_mixer, args=(accounts, follows, values["checkbox"]))
                    th_mixer.start()

def start_likes(link: str, value: int, checkbox: bool):
    global likes_counter
    likes_counter = 0
    type_of = "l"

    status = Thread(target=status_bar, args=(value, type_of))
    status.start()

    users, prxStatus = get_accounts('likes, followers')
    for login_1, values in users.items():
        if likes_counter == value:
            return

        password = values["password"]
        user_agent = values["user_agent"]

        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument("--start-maximized")
        chrome_options.add_argument("user-agent=%s" % user_agent)
        chrome_options.add_experimental_option("excludeSwitches", ['enable-automation'])
        chrome_options.headless = checkbox

        if prxStatus:
            proxy = values["proxy"]
            proxy_ip = re.findall("(.+)_\d", proxy[0])[0]
            prox = {
                "proxy": {
                    "http": "http://%s:%s@%s" % (proxy[1], proxy[2], proxy_ip)
                }
            }

            driver = webdriver.Chrome(executable_path='chromedriver.exe', options=chrome_options,
                                      seleniumwire_options=prox)
        else:
            driver = webdriver.Chrome(executable_path='chromedriver.exe', options=chrome_options)
        driver.implicitly_wait(10)
        driver.get(link)

        actions = ActionChains(driver)

        actions.click(driver.find_element(By.CLASS_NAME, "tv-social-row__start")).perform()
        time.sleep(rd(30, 60))

        actions.click(driver.find_element(By.CLASS_NAME, "js-show-email")).perform()
        fields = driver.find_elements(By.CLASS_NAME, "tv-control-material-input__wrap")
        actions.send_keys_to_element(fields[0], login_1).send_keys_to_element(fields[1], password).perform()
        actions.click(driver.find_element(By.CLASS_NAME, "tv-button__loader")).perform()

        time.sleep(10)
        likes_counter += 1
        driver.quit()

def start_follows(link: str, value: int, checkbox: bool):
    global follows_counter
    follows_counter = 0
    type_of = "f"

    status = Thread(target=status_bar, args=(value, type_of))
    status.start()

    users, prxStatus = get_accounts('likes, followers')
    for login, values in users.items():
        if follows_counter == value:
            return

        password = values["password"]
        user_agent = values["user_agent"]

        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument("--start-maximized")
        chrome_options.add_argument("user-agent=%s" % user_agent)
        chrome_options.add_experimental_option("excludeSwitches", ['enable-automation'])
        chrome_options.headless = checkbox

        if prxStatus:
            proxy = values["proxy"]
            proxy_ip = re.findall("(.+)_\d", proxy[0])[0]
            prox = {
                "proxy": {
                    "http": "http://%s:%s@%s" % (proxy[1], proxy[2], proxy_ip)
                }
            }

            driver = webdriver.Chrome(executable_path='chromedriver.exe', options=chrome_options,
                                      seleniumwire_options=prox)
        else:
            driver = webdriver.Chrome(executable_path='chromedriver.exe', options=chrome_options)

        driver.implicitly_wait(10)
        driver.get(link)

        actions = ActionChains(driver)

        actions.click(driver.find_element(By.CLASS_NAME, "js-follow-user")).perform()
        time.sleep(rd(30, 60))

        actions.click(driver.find_element(By.CLASS_NAME, "js-show-email")).perform()
        fields = driver.find_elements(By.CLASS_NAME, "tv-control-material-input__wrap")
        actions.send_keys_to_element(fields[0], login).send_keys_to_element(fields[1], password).perform()
        driver.execute_script("""
            document.querySelectorAll("[type='submit']")[0].click();
        """)

        time.sleep(10)
        follows_counter += 1
        driver.quit()

def start_comments(link: str, value: int, checkbox: bool):
    global comments_counter
    comments_counter = 0
    type_of = "c"

    status = Thread(target=status_bar, args=(value, type_of))
    status.start()

    with open('comments/comments.txt', 'r') as f:
        texts = f.read().split('\n')

    users, prxStatus = get_accounts('comments')
    for login_1, values in users.items():
        if comments_counter == value:
            return

        password = values["password"]
        user_agent = values["user_agent"]

        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument("--start-maximized")
        chrome_options.add_argument("user-agent=%s" % user_agent)
        chrome_options.add_experimental_option("excludeSwitches", ['enable-automation'])
        chrome_options.headless = checkbox

        if prxStatus:
            proxy = values["proxy"]
            proxy_ip = re.findall("(.+)_\d", proxy[0])[0]
            prox = {
                "proxy": {
                    "http": "http://%s:%s@%s" % (proxy[1], proxy[2], proxy_ip)
                }
            }
            try:
                driver = webdriver.Chrome(executable_path='chromedriver.exe', options=chrome_options,
                                      seleniumwire_options=prox)
            except:
                driver = webdriver.Chrome(executable_path='chromedriver.exe', options=chrome_options,)
        else:
            driver = webdriver.Chrome(executable_path='chromedriver.exe', options=chrome_options)
        driver.implicitly_wait(10)
        driver.get(link)

        actions = ActionChains(driver)

        comment_id = rd(0, len(texts) - 1)
        comment_text = texts[comment_id]

        text_area = driver.find_element(By.CLASS_NAME, "textarea-BQ5l96SC")
        driver.execute_script("arguments[0].scrollIntoView();", text_area)
        text_area.send_keys(comment_text)
        #actions.click(text_area).send_keys_to_element(text_area, comment_text).perform()
        actions.click(driver.find_elements(By.CLASS_NAME, "button-Gc_gGLLb")[1]).perform()
        time.sleep(rd(20, 30))
        actions.click(driver.find_element(By.CLASS_NAME, "js-show-email")).perform()
        fields = driver.find_elements(By.CLASS_NAME, "tv-control-material-input__wrap")
        actions.send_keys_to_element(fields[0], login_1).send_keys_to_element(fields[1], password).perform()
        actions.click(driver.find_element(By.CLASS_NAME, "tv-button__loader")).perform()

        time.sleep(5)

        texts.pop(comment_id)

        time.sleep(rd(110, 180))
        comments_counter += 1
        driver.quit()

def start_mixer(accounts: int, follows: int, checkbox: bool):
    global mixer_accounts
    global mixer_follows
    mixer_accounts = 0
    mixer_follows = 0
    type_of = "m"

    status = Thread(target=status_bar, args=(accounts, type_of, follows))
    status.start()

    users, prxStatus = get_accounts('mixer')
    for login, values in users.items():
        link = 'https://www.tradingview.com/u/%s/' % login
        if mixer_accounts == accounts:
            return
        for login2, value2 in users.items():
            if login == login2:
                continue
            if mixer_follows == follows:
                break

            password = value2["password"]
            user_agent = value2["user_agent"]

            chrome_options = webdriver.ChromeOptions()
            chrome_options.add_argument("--start-maximized")
            chrome_options.add_argument("user-agent=%s" % user_agent)
            chrome_options.add_experimental_option("excludeSwitches", ['enable-automation'])
            chrome_options.headless = checkbox

            if prxStatus:
                proxy = values["proxy"]
                proxy_ip = re.findall("(.+)_\d", proxy[0])[0]
                prox = {
                    "proxy": {
                        "http": "http://%s:%s@%s" % (proxy[1], proxy[2], proxy_ip)
                    }
                }

                driver = webdriver.Chrome(executable_path='chromedriver.exe', options=chrome_options,
                                          seleniumwire_options=prox)
            else:
                driver = webdriver.Chrome(executable_path='chromedriver.exe', options=chrome_options)

            driver.implicitly_wait(10)
            driver.get(link)

            actions = ActionChains(driver)

            actions.click(driver.find_element(By.CLASS_NAME, "js-follow-user")).perform()
            time.sleep(rd(30, 60))

            actions.click(driver.find_element(By.CLASS_NAME, "js-show-email")).perform()
            fields = driver.find_elements(By.CLASS_NAME, "tv-control-material-input__wrap")
            actions.send_keys_to_element(fields[0], login2).send_keys_to_element(fields[1], password).perform()
            driver.execute_script("""
                document.querySelectorAll("[type='submit']")[0].click();
            """)

            time.sleep(10)
            mixer_follows += 1
            driver.quit()
        mixer_follows = 0
        mixer_accounts += 1

def status_bar(value: int, type_of: str, value2: int = 0):
    if type_of == "l":
        layout = [
            [sg.Text("Likes: ", size=(10, 1)), sg.Text("%i of %i likes" % (likes_counter, value), key="l_progress")],
        ]
        window = sg.Window('Progress', layout)
        while True:
            events, values = window.read(100)
            if events == sg.WIN_CLOSED:
                return

            window.Element('l_progress').update("%i of %i likes" % (likes_counter, value))
    elif type_of == "f":
        layout = [
            [sg.Text("Followers: "), sg.Text("%i of %i followers" % (follows_counter, value), key = "f_progress")]
        ]
        window = sg.Window('Progress', layout)
        while True:
            events, values = window.read(100)
            if events == sg.WIN_CLOSED:
                return

            window.Element('f_progress').update("%i of %i followers" % (follows_counter, value))
    elif type_of == "c":
        layout = [
            [sg.Text("Comments: "), sg.Text(f"%s of %s comments" % (comments_counter, value), key="c_progress")]
        ]
        window = sg.Window('Progress', layout)
        while True:
            events, values = window.read(100)
            if events == sg.WIN_CLOSED:
                return

            window.Element('c_progress').update("%i of %i comments" % (comments_counter, value))
    elif type_of == "m":
        layout = [
            [sg.Text("Accounts: ", size=(10, 1)), sg.Text("%s of %s accounts" % (mixer_accounts, value), key="a_progress")],
            [sg.Text("Follows on accounts: ", size=(10, 1)), sg.Text("%s of %s follows" % (mixer_follows, value2), key="f_progress")]
        ]
        window = sg.Window('Progress', layout)
        while True:
            events, values = window.read(100)
            if events == sg.WIN_CLOSED:
                return

            window.Element('a_progress').update("%s of %s accounts" % (mixer_accounts, value))
            window.Element('f_progress').update("%s of %s follows" % (mixer_follows, value2))

if __name__ == "__main__":
    main()