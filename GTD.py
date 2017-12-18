#!/usr/local/bin/python3

import argparse
import sqlite3
from datetime import datetime

class Task(object):
    """Object representation of a GTD task"""

    def __init__( self, name, date ):
        self.name = name
        self.date = date
        self.finished = 0

class CommandLineAPI(object):
    """Command-line GTD utility"""

    def __init__( self ):
        self.connection = sqlite3.connect( "/Users/Sensei/Library/GTD/GTD.db" )
        self.cursor = self.connection.cursor()

    def ls( self ):
        for row in self.cursor.execute( "SELECT * FROM tasks" ):
            print( row )
        self.connection.close()

    def add( self, name, date ):

        if( date == None ):
            self.cursor.execute( "INSERT INTO tasks (name) VALUES (?)", [name] )
        else:
            print( datetime.strptime( date, "%d.%m.%Y" ) )
            self.cursor.execute( "INSERT INTO tasks (name, due_date) \
                                  VALUES (?, ?)", [ name, datetime.strptime( date, "%d.%m.%Y" ) ] )
        self.connection.commit()
        self.connection.close()


parser = argparse.ArgumentParser()
subparsers = parser.add_subparsers( help="List of commands", dest="cmd" );

ls = subparsers.add_parser( 'ls', help="Lists tasks" );
ls.add_argument( "-t", "--task", help="Task Name" );
ls.add_argument( "-d", "--date", help="Due date of task" );

add = subparsers.add_parser( 'add', help="Adds a task" );
add.add_argument( "-t", "--task", required=True, help="Task Name" );
add.add_argument( "-d", "--date", help="Due date of task" );

remove = subparsers.add_parser( 'remove', help="Removes a task" );
remove.add_argument( "-i", "--id", type=int, help="Task ID" );

args = parser.parse_args()
print( args )

if( args.cmd == "add" ):
    CommandLineAPI().add( args.task, args.date );
elif( args.cmd == "ls" ):
    CommandLineAPI().ls();
else:
    print( "WIP" )
