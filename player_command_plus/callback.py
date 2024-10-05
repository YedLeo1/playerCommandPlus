import time
from mcdreforged.api.types import CommandSource
from mcdreforged.api.all import *

from player_command_plus import utils, global_var


def loadplayer(conn,elem):
    playerlist=utils.getplayer(conn)
    while elem.lower() not in playerlist.lower():
        playerlist=utils.getplayer(conn)
        time.sleep(0.05)


@new_thread('PlayerCommandPlus')
def OperateBots(source:CommandSource,ctx):

    global ss
    conn = utils.RconInit()

    if not source.is_player:
        source.reply("只有玩家可使用")
        return
    action:str = ctx["action"]
    botName = ctx["name"]
    server = source.get_server()
    #处理假人列表
    BotList = []
    #初始化假人列表
    Index = botName.find("[")
    actionArray = action.split(".")

    if actionArray[0] == "spawnn":
        start = 1
        playerlist = utils.getplayer(conn)
        while botName[:Index] + str(start) in playerlist.lower():
            start+=1
        for i in range(256):
            BotList.append(botName[:Index] + str(i + start))
    elif actionArray[0] == "full":
        # action = action.replace(".", " ", -1)
        # source.reply(action)
        x1 = int(actionArray[1])
        y1 = int(actionArray[2])
        x2 = int(actionArray[3])
        y2 = int(actionArray[4])
        if x1>x2 and y1>y2:
            start = int(x1 - x2) + 1
            end = int(y1 - y2) + 1
        elif (x1>x2 and y1<y2)or(x1<x2 and y1>y2):
            start = int(max(x2,x1)-min(x2,x1))+1
            end = int(max(y2,y1)-min(y2,y1))+1
        else:
            start = int(x2-x1)+1
            end = int(y2-y1)+1

        qq = 1
        playerlist = utils.getplayer(conn)
        while botName[:Index] + str(qq) in playerlist.lower():
            qq+=1

        for i in range(end * start):
            BotList.append(botName[:Index] + str(i+qq))
    elif actionArray[0] == "full1":
        # action = action.replace(".", " ", -1)
        # source.reply(action)
        x1 = int(actionArray[1])
        y1 = int(actionArray[2])
        x2 = int(actionArray[3])
        y2 = int(actionArray[4])
        if x1>x2 and y1>y2:
            start = int(x1 - x2) + 1
            end = int(y1 - y2) + 1
        elif (x1>x2 and y1<y2)or(x1<x2 and y1>y2):
            start = int(max(x2,x1)-min(x2,x1))+1
            end = int(max(y2,y1)-min(y2,y1))+1
        else:
            start = int(x2-x1)+1
            end = int(y2-y1)+1

        qq = 1
        playerlist = utils.getplayer(conn)
        while botName[:Index] + str(qq) in playerlist.lower():
            qq+=1

        for i in range(start):
            BotList.append(botName[:Index] + str(i+qq))
    elif Index>0:
        if actionArray[0] == "load" and len(actionArray) >= 6:
            if (actionArray[1] == "max"):
                BotList.append(botName[:Index])
            else:
                ranges = botName[Index + 1:-1].split("-")
                start = int(ranges[0])
                end = int(ranges[1]) + 1

                for i in range(end - start):
                    BotList.append(botName[:Index] + str(i + start))
        else:
            ranges = botName[Index+1:-1].split("-")
            start = int(ranges[0])
            end = int(ranges[1])+1

            for i in range(end-start):
                BotList.append(botName[:Index]+str(i+start))
    else:

        if botName.find("]")>0:
            source.reply("名称错误")
            return
        BotList.append(botName)

    #生成假人

    if actionArray[0] == "spawn":
        pos,dimesion,Rotation,gamemode=utils.init(conn, source.player)

        for elem in BotList:
            spawnStr = "player {} spawn at {} {} {} facing {} {} in {} in {}".format(elem,pos.x,pos.y,pos.z,Rotation[0],Rotation[1],dimesion,gamemode)
            server.execute(spawnStr)
            loadplayer(conn,elem)

        return
    elif actionArray[0] == "init":
        pos,dimesion,Rotation,gamemode=utils.init(conn, source.player)

        for elem in BotList:

            spawnStr = "player {} spawn at {} {} {} facing {} {} in {} in {}".format(elem, pos.x, pos.y, pos.z,
                                                                                     Rotation[0], Rotation[1], dimesion,
                                                                                     gamemode)
            server.execute(spawnStr)

            loadplayer(conn,elem)

            # source.reply(elem.lower())
            # time.sleep(0.2)
            spawnStr = "player {} kill".format(elem)
            server.execute(spawnStr)
        return
    elif actionArray[0] == "full1":
        pos,dimesion,Rotation,gamemode=utils.init(conn, source.player)
        x1 = int(actionArray[1])
        y1 = int(actionArray[2])
        x2 = int(actionArray[3])
        y2 = int(actionArray[4])

        if x1>x2 and y1>y2:
            x1,x2=x2,x1
            y1,y2=y2,y1

        x=min(x1,x2)
        y=min(y1,y2)

        for elem in BotList:
            if x>max(x1,x2):
                x=min(x1,x2)
                y+=1

            spawnStr = "player {} spawn at {} {} {} facing 0 180 in {} in survival".format(elem, x+0.5, pos.y, y+0.5, dimesion)
            server.execute(spawnStr)
            x+=1

            loadplayer(conn,elem)

        return
    elif actionArray[0] == "a":
        pos, dimesion, Rotation, gamemode = utils.init(conn, source.player)

        x1 = int(pos.x)
        y1 = int(pos.z)

        if (x1 >= 0):
            x11 = x1%16
        else:
            x11 = 16 - (-x1 % 16)

        if (y1 >= 0):
            y11 = y1%16
        else:
            y11 = 16 - (-y1 % 16)
        source.reply(utils.maxhigh(x1, y1)[y11][x11])

    elif actionArray[0] == "keep":
        BotList1=BotList
        playerlist = utils.getplayer(conn)
        first=BotList1[0]

        if first in playerlist:
            pos = utils.GetPlayerLocation(conn,first)
        elif first.lower() in playerlist:
            pos = utils.GetPlayerLocation(conn,first.lower())
        elif first.upper() in playerlist:
            pos = utils.GetPlayerLocation(conn,first.upper())

        x = pos.x - (pos.x % 16)+0.5
        z = pos.z - (pos.z % 16)+0.5

        # source.reply(x)
        # source.reply(z)
        #
        p = 0
        while True:
            i = 0
            for elem in BotList1:
                # source.reply(elem)
                if i % 16 == 0:
                    p=1-p
                if i%2==p:
                    i+=1
                    continue


                if elem in playerlist:
                    pos = utils.GetPlayerLocation(conn,elem)

                elif elem.lower() in playerlist:
                    pos = utils.GetPlayerLocation(conn,elem.lower())

                elif elem.upper() in playerlist:
                    pos = utils.GetPlayerLocation(conn,elem.upper())
                else:

                    for elem1 in BotList1:
                        spawnStr = "player {} kill".format(elem1)
                        server.execute(spawnStr)
                    return

                print(1)
                if pos.x != x+(i - i % 16) / 16 or pos.z != z+i % 16:
                    for elem1 in BotList1:
                        spawnStr = "player {} kill".format(elem1)
                        server.execute(spawnStr)

                    return
                i += 1
    elif actionArray[0] == "load":
        pos,dimesion,Rotation,gamemode=utils.init(conn, source.player)
        time.sleep(1)


        for elem in BotList:
            spawnStr = "player {} spawn at {} {} {} facing {} {} in {} in {}".format(elem, pos.x, pos.y, pos.z,
                                                                                     Rotation[0], Rotation[1], dimesion,
                                                                                     gamemode)
            server.execute(spawnStr)

            loadplayer(conn,elem)

            time.sleep(0.2)
            spawnStr = "player {} kill".format(elem)
            server.execute(spawnStr)
            time.sleep(0.85)

        return
    elif actionArray[0] == "drop1":

        for elem in BotList:

            spawnStr = "player {} dropStack all".format(elem)
            server.execute(spawnStr)

        return
    elif actionArray[0] == "drop2":
        start=1

        if len(actionArray)==2:
            start = actionArray[1]
        for elem in BotList:
            for i in range(int(start),35):
                spawnStr = "player {} dropStack {}".format(elem,i)
                server.execute(spawnStr)

        return
    elif actionArray[0] == "spawnn":
        pos,dimesion,Rotation,gamemode=utils.init(conn, source.player)

        x=pos.x - (pos.x % 16)
        z=pos.z - (pos.z % 16)
        y=utils.maxhigh(x,z)
        i=0
        for elem in BotList:

            spawnStr = "player {} spawn at {} {} {} facing 0 180 in {} in survival".format(elem,x+(i-i%16)/16+0.5,utils.max_y(y,x+(i-i%16)/16,z+i%16),z+i%16+0.5,dimesion)



            server.execute(spawnStr)
            i+=1
            loadplayer(conn,elem)

        return
    elif actionArray[0] == "full":
        pos,dimesion,Rotation,gamemode=utils.init(conn, source.player)
        x1 = int(actionArray[1])
        y1 = int(actionArray[2])
        x2 = int(actionArray[3])
        y2 = int(actionArray[4])

        if x1>x2 and y1>y2:
            x1,x2=x2,x1
            y1,y2=y2,y1

        x=min(x1,x2)
        y=min(y1,y2)

        for elem in BotList:
            if x>max(x1,x2):
                x=min(x1,x2)
                y+=1

            spawnStr = "player {} spawn at {} {} {} facing 0 180 in {} in survival".format(elem, x+0.5, pos.y, y+0.5, dimesion)
            server.execute(spawnStr)
            x+=1

            loadplayer(conn,elem)

        return
    elif actionArray[0] == "ac":
        for elem in BotList:
            spawnStr = "player {} attack continuous".format(elem)
            server.execute(spawnStr)
        return
    else:
        if actionArray[0] not in global_var.vaild_action_dict:
            source.reply("未知的action")
            return
        action = action.replace("."," ",-1)
        prefix = "" if global_var.serverConfig["prefix"]=="#none" else global_var.serverConfig["prefix"]
        suffix = "" if global_var.serverConfig["suffix"]=="#none" else global_var.serverConfig["suffix"]
        for elem in BotList:
            server.execute("player {} {}".format(prefix+elem+suffix,action))
        return

def Help(source:CommandSource):
    source.reply(
'''
------------PlayerCommandPlus
1-!!pcp help 显示该消息
2-!!pcp name[范围] [操作]
  例1-!!pcp hello spawn 
  召唤名为hello假人
  例2-!!pcp hello[0-2] spawn 
  召唤名为 hello0,hello1,hello2的假人
  例3-!!pcp hello[0-2] jump.interval.10
  让hello0,hello1,hello2假人每10gt跳一次
  例4-!!pcp a[] spawnn
  让假人挖掘这一区块的方块
  例5-!!pcp a[1-256] init
  预加载假人数据
  例5-!!pcp a[1-256] ac
  让假人挖掘
  例6-!!pcp a[1-256] full.x1.y1.x2.y2
  让假人生成在(x1,y1)(x2,y2)直接的方块上
  -----------------------------''')