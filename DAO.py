#!/usr/local/bin/python3

class Constants:
    CMDS = [ "add", "ls", "del", "upd" ]

def execute( cmd ):

    if not cmd.name in Constants.CMDS:
        raise Exception( "error: command '{}' is not a valid command".format( 
                         cmd.name ) )

    tname  = cmd.task_name if cmd.task_name != None else "None"
    tdate  = cmd.task_date if cmd.task_date != None else "None"
    tindex = int( cmd.task_index ) if cmd.task_index != None else -1

    if cmd.name == "add":
        print( "Added new task '{}' on date '{}'".format( tname, tdate ) )
    elif cmd.name == "ls":
        print( "Listing task '{}' on date '{}'".format( tname, tdate ) )
    elif cmd.name == "del":
        print( "Deleting task  '{}' on date '{}'".format( tname, tdate ) )
    elif cmd.name == "upd":
        print( "Updating task '{}' on date '{}'".format( tname, tdate ) )
