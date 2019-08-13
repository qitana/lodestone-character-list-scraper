import sys
import re
import time
import requests
import sqlite3
from bs4 import BeautifulSoup
from enum import Enum, auto


class DC(Enum):
    Elemental = '_dc_Elemental'
    Gaia = '_dc_Gaia'
    Mana = '_dc_Mana'
    Aether = '_dc_Aether'
    Primal = '_dc_Primal'
    Crystal = '_dc_Crystal'
    Chaos = '_dc_Chaos'
    Light = '_dc_Light'


class WorldName(Enum):
    Adamantoise = 1
    Aegis = 2
    Alexander = 3
    Anima = 4
    Asura = 5
    Atomos = 6
    Bahamut = 7
    Balmung = 8
    Behemoth = 9
    Belias = 10
    Brynhildr = 11
    Cactuar = 12
    Carbuncle = 13
    Cerberus = 14
    Chocobo = 15
    Coeurl = 16
    Diabolos = 17
    Durandal = 18
    Excalibur = 19
    Exodus = 20
    Faerie = 21
    Famfrit = 22
    Fenrir = 23
    Garuda = 24
    Gilgamesh = 25
    Goblin = 26
    Gungnir = 27
    Hades = 28
    Hyperion = 29
    Ifrit = 30
    Ixion = 31
    Jenova = 32
    Kujata = 33
    Lamia = 34
    Leviathan = 35
    Lich = 36
    Louisoix = 37
    Malboro = 38
    Mandragora = 39
    Masamune = 40
    Mateus = 41
    Midgardsormr = 42
    Moogle = 43
    Odin = 44
    Omega = 45
    Pandaemonium = 46
    Phoenix = 47
    Ragnarok = 48
    Ramuh = 49
    Ridill = 50
    Sargatanas = 51
    Shinryu = 52
    Shiva = 53
    Siren = 54
    Spriggan = 55
    Tiamat = 56
    Titan = 57
    Tonberry = 58
    Twintania = 59
    Typhon = 60
    Ultima = 61
    Ultros = 62
    Unicorn = 63
    Valefor = 64
    Yojimbo = 65
    Zalera = 66
    Zeromus = 67
    Zodiark = 68


class ClassJob(Enum):
    GLD = 1
    PGL = 2
    MRD = 3
    LNC = 4
    ARC = 5
    CNJ = 6
    THM = 7
    CRP = 8
    BSM = 9
    ARM = 10
    GSM = 11
    LTW = 12
    WVR = 13
    ALC = 14
    CUL = 15
    MIN = 16
    BTN = 17
    FSH = 18
    PLD = 19
    MNK = 20
    WAR = 21
    DRG = 22
    BRD = 23
    WHM = 24
    BLM = 25
    ACN = 26
    SMN = 27
    SCH = 28
    ROG = 29
    NIN = 30
    MCH = 31
    DRK = 32
    AST = 33
    SAM = 34
    RDM = 35
    BLU = 36
    GNB = 37
    DNC = 38


class Race(Enum):
    Hyur = 'race_1'
    Elezen = 'race_2'
    Lalafell = 'race_3'
    Miqote = 'race_4'
    Roegadyn = 'race_5'
    AuRa = 'race_6'
    Hrothgar = 'race_7'
    Viera = 'race_8'


class Tribe(Enum):
    Midlander = 'tribe_1'
    Highlander = 'tribe_2'
    Wildwood = 'tribe_3'
    Duskwight = 'tribe_4'
    Plainsfolk = 'tribe_5'
    Dunesfolk = 'tribe_6'
    SeekerOfTheSun = 'tribe_7'
    KeeperOfTheMoon = 'tribe_8'
    SeaWolf = 'tribe_9'
    Hellsguard = 'tribe_10'
    Raen = 'tribe_11'
    Xaela = 'tribe_12'
    Helions = 'tribe_13'
    TheLost = 'tribe_14'
    Rava = 'tribe_15'
    Veena = 'tribe_16'


class Gcid(Enum):
    NoAffiliation = 0
    Maelstrom = 1
    OrderOfTheTwinAdder = 2
    ImmortalFlames = 3


class Lang(Enum):
    ja = auto()
    en = auto()
    de = auto()
    fr = auto()


class Orders(Enum):
    NameAtoZ = 1
    # NameZtoA = 2
    # WorldAtoZ = 3
    # WorldZtoA = 4
    # LevelLowtoHigh = 5
    # LevelHighToLow = 6


if __name__ == '__main__':

    args = sys.argv
    serverId_start = 0
    serverId_end = 256

    if len(args) > 3:
        if (args[1].isdecimal() & args[2].isdecimal()):
            serverId_start = int(args[1])
            serverId_end = int(args[2])

    dbname = 'db.sqlite3'
    connection = sqlite3.connect(dbname)
    cursor = connection.cursor()
    cursor.execute(
        "CREATE TABLE IF NOT EXISTS lodestone (id INTEGER PRIMARY KEY, name TEXT, server TEXT, dc TEXT)")

    baseUrl = 'https://jp.finalfantasyxiv.com/lodestone/character/?q='
    ua = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36'
    headers = {'User-Agent': ua}
    cookies = requests.cookies.RequestsCookieJar()
    alphabets = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L',
                 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']

    for worldName in WorldName:
        if (worldName.value < serverId_start) | (worldName.value > serverId_end):
            continue
        for classJob in ClassJob:
            for tribe in Tribe:
                for gcid in Gcid:
                    for lang in Lang:
                        for alphabet in alphabets:
                            for order in Orders:

                                search_url = baseUrl + alphabet + \
                                    '&worldname=' + worldName.name + \
                                    '&classjob=' + str(classJob.value) + \
                                    '&race_tribe=' + str(tribe.value) + \
                                    '&gcid=' + str(gcid.value) + \
                                    '&lang=' + lang.name + \
                                    '&order=' + str(order.value)
                                # print(search_url)

                                currentPage = 1
                                totalPage = 1
                                totalCount = 0
                                for page in range(1, 20):
                                    if page > totalPage:
                                        break

                                    url = search_url + '&page=' + str(page)
                                    print('[INFO] URL:', url)
                                    try:
                                        response = requests.get(
                                            url, headers=headers, cookies=cookies, timeout=(15.0, 60.0))
                                        response.encoding = response.apparent_encoding
                                    except:
                                        print(
                                            '[ERROR] Failed to get data from url.', url)
                                        continue

                                    for c in response.cookies:
                                        cookies.set_cookie(c)

                                    try:
                                        bs = BeautifulSoup(
                                            response.text, 'html.parser')
                                        for i in bs.select("div.ldst__bg div.ldst__contents.clearfix div.ldst__main div.ldst__window div.select-pulldown__count div.parts__total"):
                                            totalCount = int(
                                                re.sub("\\D", "", i.getText()))

                                        for i in bs.select("div.ldst__bg div.ldst__contents.clearfix div.ldst__main div.ldst__window ul.btn__pager li.btn__pager__current"):
                                            s = i.getText().split('/')
                                            if len(s) == 2:
                                                currentPage = int(
                                                    re.sub("\\D", "", s[0].strip()))
                                                totalPage = int(
                                                    re.sub("\\D", "", s[1].strip()))

                                        #print('currentPage=', currentPage)
                                        #print('totalPage=', totalPage)
                                        #print('totalCount=', totalCount)

                                        for i in bs.select("div.ldst__bg div.ldst__contents.clearfix div.ldst__main div.ldst__window div.entry"):
                                            character_lodestone_id = ''
                                            character_name = ''
                                            character_world = ''
                                            character_dc = ''

                                            for j in i.select("a.entry__link"):
                                                link = j.get("href").split('/')
                                                if len(link) == 5:
                                                    if(link[1] == 'lodestone') & (link[2] == 'character'):
                                                        character_lodestone_id = link[3]
                                            for j in i.select("p.entry__name"):
                                                character_name = j.getText()
                                            for j in i.select("p.entry__world"):
                                                world_dc = j.getText().split()
                                                if len(world_dc) == 2:
                                                    character_world = world_dc[0]
                                                    character_dc = world_dc[1].replace(
                                                        '(', '').replace(')', '')
                                            try:
                                                cursor.execute("REPLACE INTO lodestone VALUES (?, ?, ?, ?)", (
                                                    character_lodestone_id, character_name, character_world, character_dc))
                                                connection.commit()
                                            except:
                                                print('[ERROR] Failed to write to db.', (
                                                    character_lodestone_id, character_name, character_world, character_dc))

                                            # print(character_lodestone_id, character_name, character_world, character_dc, sep=', ')
                                    except:
                                        print(
                                            '[ERROR] Failed to parse html.', url)
                                        print(
                                            '-----------------------------', url)
                                        print(response.text)
                                        print(
                                            '-----------------------------', url)
                                        continue

                                    time.sleep(5)

    connection.commit()
    connection.close()
    print('[INFO] COMPLETE.')
