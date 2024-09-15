import minecraft_data_api as api
from mcdreforged.api.types import CommandSource
from mcdreforged.minecraft.rcon.rcon_connection import RconConnection
import parse
import re
import hjson
import collections

Coordinate = collections.namedtuple('Coordinate', 'x y z')


def remove_letter_after_number(text: str) -> str:
    result = ''
    while text:
        pos = min(text.find('"'), text.find("'"))
        quote = None
        if pos == -1:
            pos = len(text)
        non_quote_str, quote_str = text[:pos], text[pos:]
        non_quote_str = re.sub(r'(?<=\d)[a-zA-Z](?=(\D|$))', '',
                               non_quote_str)  # remove letter after number outside string: 1.23D
        non_quote_str = re.sub(r'(?<=\[)[IL];', '',
                               non_quote_str)  # remove int array or long array header outside string: [I: 1,2,3]
        result += non_quote_str
        if quote_str:
            quote = quote_str[0]
            result += quote
            quote_str = quote_str[1:]  # remove the beginning quote
        while quote_str:
            slash_pos = quote_str.find('\\')
            if slash_pos == -1:
                slash_pos = len(quote_str)
            quote_pos = quote_str[:slash_pos].find(quote)
            if quote_pos == -1:  # cannot find a quote in front of the first slash
                if slash_pos == len(quote_str):
                    raise ValueError('Cannot find a string ending quote')
                result += quote_str[:slash_pos + 2]
                quote_str = quote_str[slash_pos + 2:]
            else:
                result += quote_str[:quote_pos + 1]
                quote_str = quote_str[quote_pos + 1:]  # found an un-escaped quote
                break
        text = quote_str
    return result

def CheckBrackets(str:str):
    stack = []
    for i in range(len(str)):
        if str[i]=="[":
            stack.append(i)
            continue
        elif str[i]=="]":
            if not stack:
                return False
            else:
                stack.pop()
                continue
    return len(stack) == 0

def GetPlayerLocation(conn,name):
    pos=getplayerinfo(conn, name, "Pos")
    return Coordinate(x=float(pos[0]), y=float(pos[1]), z=float(pos[2]))

def GetPlayerDimesion(conn,name):
    #return ["minecraft:overworld","minecraft:the_end","minecraft:the_nether"][api.get_player_dimension(name)]
    dimesion = getplayerinfo(conn,name,"Dimension")
    return dimesion

def GetPlayerGamemode(conn,name):
    # print(getplayerinfo(conn,name,"playerGameType"))
    return getplayerinfo(conn,name,"playerGameType")

def GetPlayerRotation(conn,name):
    return getplayerinfo(conn,name,"Rotation")

def LoadConfig():
    global config

    with open('./server/server.properties', 'r', encoding="utf-8") as file:
        for line in file:
            stripped_line = line.strip()
            if stripped_line.startswith('rcon.password='):
                rcon_password = stripped_line.split('=')[1]
            if stripped_line.startswith('rcon.port='):
                rcon_port = stripped_line.split('=')[1]
    return rcon_password,rcon_port

def RconInit():
    rcon_password,rcon_port=LoadConfig()
    # print(rcon_password,rcon_port)
    Rcon = RconConnection("localhost", int(rcon_port), str(rcon_password))
    Rcon.connect()
    return Rcon

def getplayer(conn):
    info = conn.send_command("list")

    formatters = (
        # <1.16
        # There are 6 of a max 100 players online: 122, abc, xxx, www, QwQ, bot_tob
        r'There are {amount:d} of a max {limit:d} players online:{players}',
        # >=1.16
        # There are 1 of a max of 20 players online: Fallen_Breath
        r'There are {amount:d} of a max of {limit:d} players online:{players}',
    )
    for formatter in formatters:
        parsed = parse.parse(formatter, info)
        if parsed is not None and parsed['players'].startswith(' '):
            return parsed['players']

def getplayerinfo(conn,player,path):

    text = conn.send_command("data get entity {} {}".format(player, path))
    text = re.sub(r'^.* has the following entity data: ', '', text)  # yeet prefix

    text = remove_letter_after_number(text)

    value = hjson.loads(text)


    return value


