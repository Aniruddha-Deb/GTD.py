#!/usr/local/bin/python3

from parser import Constants

def execute_add_command( cmd ):
    print( "INSERT INTO tasks (name, due_date) VALUES ({}, {})".format( cmd.task_name.value, cmd.task_date.value ) )

op_map = { "-lt": "<",
           "-le": "<=",
           "-gt": ">",
           "-ge": ">=",
           "-eq": "=",
           "-ne": "!=" }

def add_parameters_to_statement( cmd, stmt ):
    if cmd.task_name != None or cmd.task_date != None or cmd.task_index != None:
        stmt.append( "WHERE" )
        add_task_parameter_to_statement( cmd, stmt )
        add_date_parameter_to_statement( cmd, stmt )
        add_id_parameter_to_statement( cmd, stmt ) 
    return stmt

def add_task_parameter_to_statement( cmd, stmt ):
    if cmd.task_name != None:
        if "date" in stmt or "id" in stmt:
            stmt.append( "AND" )
        stmt.append( "task" )
        if cmd.task_name.regexp == True:
            stmt.append( "REGEXP" )
        elif cmd.task_name.like == True:
            stmt.append( "LIKE" )
        else:
            stmt.append( "=" )
        stmt.append( "?" )

def add_date_parameter_to_statement( cmd, stmt ):
    if cmd.task_date != None :
        if "task" in stmt or "id" in stmt:
            stmt.append( "AND" )
        stmt.append( "date" )
        add_numeric_parameter_to_statement( cmd, stmt )

def add_id_parameter_to_statement( cmd, stmt ):
    if cmd.task_index != None:
        if "task" in stmt or "date" in stmt:
            stmt.append( "AND" )
        stmt.append( "id" )
        add_numeric_parameter_to_statement( cmd, stmt )

def add_numeric_parameter_to_statement( cmd, stmt ):
    if cmd.task_index.comparator != None:
        stmt.append( op_map[cmd.task_index.comparator] )
    else:
        stmt.append( "=" )
    stmt.append( "?" )
  
def execute_ls_command( cmd ):

    stmt = [ "SELECT", "*", "FROM", "tasks" ]
    add_parameters_to_statement( cmd, stmt )
    print( " ".join( stmt ) )

def execute_del_command( cmd ):
    
    stmt = [ "DELETE", "FROM", "tasks" ]
    add_parameters_to_statement( cmd, stmt )
    print( " ".join( stmt ) )

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