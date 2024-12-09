import json
import datetime
# import logging
import sqlite3

class config():
    def __init__(self):
        with open('config/config.json') as json_file:
            jsonstructure = json.load(json_file)
            for p in jsonstructure['discord']:
                self.token = p['token']
                self.pterodactyl_domain = p['pterodactyl_domain']
                self.pterodactyl_apikey = p['pterodactyl_apikey']
                # self.mod_roles = p['mod_roles']
                # self.admin_roles = p['admin_roles']

    def get_token(self):
        return self.token
    def get_pterodactyl_domain(self):
        return self.pterodactyl_domain
    def get_pterodactyl_apikey(self):
        return self.pterodactyl_apikey
    # def get_mod_roles(self):
    #     return self.mod_roles
    # def get_admin_roles(self):
    #     return self.admin_roles
    

con = sqlite3.connect('data/database.sqlite')
cur = con.cursor()
cur.execute("""CREATE TABLE IF NOT EXISTS user (id INT PRIMARY KEY, nickname TEXT, avatar_url TEXT, mcname TEXT, uuid TEXT, iswhitelisted BOOLEAN, )""") 

# def logger():
#     day = datetime.datetime.now()

#     logfile = f'logs/discord_{str(day.year)}_{str(day.month)}_{str(day.day)}.log'
#     logger = logging.getLogger('discord')
#     logger.setLevel(logging.WARNING)
#     handler = logging.FileHandler(filename=logfile, encoding='utf-8', mode='w')
#     handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
#     logger.addHandler(handler)

def getdb():
    return (con, cur)