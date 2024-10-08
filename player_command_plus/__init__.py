from mcdreforged.api import command
from mcdreforged.api.types import PluginServerInterface
import os
import json
from .callback import *
from .global_var import *

const ={
    "configFilePath":"config/player_command_plus.json",
}
DefaultConfig = {
        "prefix":"#none",
        "suffix":"#none"
}

def on_load(server:PluginServerInterface,old):
    GenerateConfigFile()
    SetGlobals(server,ReadConfigFile())
    RegistCommand(server)
    server.register_help_message("!!pcp","你的批量假人助手")


def GenerateConfigFile():
    if os.path.exists(const["configFilePath"]) == False:
        with open(const["configFilePath"],"x",-1) as file:
            file.write(json.dumps(DefaultConfig))
        return
    return

def ReadConfigFile():
    with open(const["configFilePath"],"r",-1) as file:
        config = json.loads(file.read())
        return config
    
def RegistCommand(server):
    b = command.SimpleCommandBuilder()
    '''command'''
  
    b.command("!!pcp <name> <action>",callback.OperateBots) #支持正则
    
    #help
    b.command("!!pcp help",callback.Help)
    b.command("!!pcp",callback.Help)
    '''args'''
    b.arg("name",command.Text)
    #b.arg("count",command.Integer)
    b.arg("action",command.Text)
    '''regist'''
    b.register(server)
    return

