#!/usr/local/bin/python3

from datetime import datetime, timedelta

from parser import Constants

def execute( cmd ):

    if not cmd.name in Constants.CMDS:
        raise Exception( "error: command '{}' is not a valid command".format( 
                         cmd.name ) )

    # TODO use polymorphism here instead of if-else
    if cmd.name == "add":
        execute_add_command( cmd )
    elif cmd.name == "ls":
        execute_ls_command( cmd )
    elif cmd.name == "del":
        execute_del_command( cmd )
    elif cmd.name == "upd":
        execute_upd_command( cmd )
    elif cmd.name == "today":
        execute_today_command( cmd )

def execute_add_command( cmd ):

    sanitize_command_for_add( cmd )
    tdate = datetime.now().date().strftime( "%d.%m.%Y" )
    if cmd.task_date != None and cmd.task_date.value != None:
        tdate = process_date( cmd.task_date.value )

    print( "INSERT INTO tasks (name, due_date) VALUES ({}, {})".format( cmd.task_name.value, tdate ) )

def process_date( date ):
    if date.startswith( "t" ):
        today = datetime.now().date()
        if len( date ) > 2:
            numDays = int( date[2:] )
            today = eval( "today " + date[1] + "timedelta({})".format( numDays ) )
        return today.strftime( "%d.%m.%Y" )
    else:
        return date

def sanitize_command_for_add( cmd ):
    if cmd.task_name == None or cmd.task_name.value == None:
        raise Exception( "error: 'add' command requires a task name" )
    if cmd.task_name.regexp == True or cmd.task_name.like == True:
        print( "warning: regexp tag or like tag are not required in 'add'." )
    if cmd.task_date != None and cmd.task_date.comparator != None:
        print( "warning: comparator tag is not required in 'add'." )
    if cmd.task_index != None:
        print( "warning: index parameter is not required in 'add'." )

def execute_ls_command( cmd ):
    pass

def execute_del_command( cmd ):
    pass

def execute_upd_command( cmd ):
    pass

def execute_today_command( cmd ):
    pass