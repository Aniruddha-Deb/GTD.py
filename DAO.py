#!/usr/local/bin/python3

from datetime import datetime, timedelta

from parser import Constants

def execute_add_command( cmd ):

    sanitize_command_for_add( cmd )
    tdate = process_date( cmd.task_date )

    print( "INSERT INTO tasks (name, due_date) VALUES ({}, {})".format( cmd.task_name.value, tdate ) )

# TODO find an elegant way to sanitize the inputs
def sanitize_command_for_add( cmd ):
    if cmd.task_name == None or cmd.task_name.value == None:
        raise Exception( "error: 'add' command requires a task name" )
    if cmd.task_name.regexp == True or cmd.task_name.like == True:
        print( "warning: regexp tag or like tag are not required in 'add'." )
    if cmd.task_date != None and cmd.task_date.comparator != None:
        print( "warning: comparator tag is not required in 'add'." )
    if cmd.task_index != None:
        print( "warning: index parameter is not required in 'add'." )

def process_date( date ):
    today = datetime.now().date()
    if date == None or date.value == None:
        return today.strftime( "%d.%m.%Y" )
    elif date.value.startswith( "t" ):
        if len( date.value ) > 2:
            numDays = int( date[2:] )
            today = eval( "today " + date[1] + "timedelta({})".format( numDays ) )
        return today.strftime( "%d.%m.%Y" )
    else:
        return date

def execute_ls_command( cmd ):
    pass

def execute_del_command( cmd ):
    pass

def execute_upd_command( cmd ):
    pass

def execute_today_command( cmd ):
    pass

cmds = { "add"  : execute_add_command,
         "ls"   : execute_ls_command,
         "del"  : execute_del_command,
         "upd"  : execute_upd_command,
         "today": execute_today_command }

def execute( cmd ):

    if not cmd.name in Constants.CMDS:
        raise Exception( "error: command '{}' is not a valid command".format( 
                         cmd.name ) )

    cmds[cmd.name](cmd)