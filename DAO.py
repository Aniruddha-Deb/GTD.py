#!/usr/local/bin/python3

from parser import Constants

def execute_add_command( cmd ):

    print( "INSERT INTO tasks (name, due_date) VALUES ({}, {})".format( cmd.task_name.value, cmd.task_date.value ) )

op_map = { "-lt": " <",
           "-le": " <=",
           "-gt": " >",
           "-ge": " >=",
           "-eq": " =",
           "-ne": " !=" }

def execute_ls_command( cmd ):

    # TODO: Clean up this terrible piece of crap.
    stmt = "SELECT * FROM tasks"
    if cmd.task_name != None or cmd.task_date != None or cmd.task_index != None:
        stmt += " WHERE"
        added_task = False
        if cmd.task_name != None:
            stmt += " task"
            added_task = True
            if cmd.task_name.regexp == True:
                stmt += " REGEXP"
            elif cmd.task_name.like == True:
                stmt += " LIKE"
            else:
                stmt += " ="
            stmt += " ?"
        if cmd.task_date != None :
            if added_task:
                stmt += " AND"
            else:
                added_task = True
            stmt += " date"
            if cmd.task_date.comparator != None:
                stmt += op_map[cmd.task_date.comparator]
            else:
                stmt += " ="
            stmt += " ?"
        if cmd.task_index != None:
            if added_task:
                stmt += " AND"
            stmt += " id"
            if cmd.task_index.comparator != None:
                stmt += op_map[cmd.task_index.comparator]
            else:
                stmt += " ="
            stmt += " ?"
    print( stmt )

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