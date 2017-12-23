#!/usr/local/bin/python3

from argparse import ArgumentParser
import sqlite3
from datetime import datetime

from parser import parser

class CommandLineAPI(object):
    """Command-line GTD utility"""

    def __init__( self ):
        self.connection = sqlite3.connect( "/Users/Sensei/Library/GTD/GTD.db" )
        self.cursor = self.connection.cursor()

    def ls( self, task=None, date=None ):
        print( "Task = %s and date = %s" % (task, date) )
        print( parser.prepareStatement( 
            parser.StatementType.SELECT, ["task", "due_date"], [task,date] ) )
        for row in self.cursor.execute( parser.prepareStatement( 
            parser.StatementType.SELECT, ["task", "due_date"], [task,date] ) ):
            row_id = format( row[0], "<3" ) + "| "
            row_task = format( row[1], "<40" ) + "| "
            row_date = " "
            if row[2] != None:
                row_date = format( row[2], "<" ) 
            print( row_id + row_task + row_date )
        self.connection.close()

    def add( self, name, date ):
        if( date == None ):
            self.cursor.execute( "INSERT INTO tasks (name, due_date) \
                                  VALUES (?, ?)", [name, str( datetime.now().strftime( "%d.%m.%Y" ) )] )
        else:
            print( datetime.strptime( date, "%d.%m.%Y" ) )
            self.cursor.execute( "INSERT INTO tasks (name, due_date) \
                                  VALUES (?, ?)", [name, date] )
        self.connection.commit()
        self.connection.close()

    def remove( self, id=None, date=None ):
        self.cursor.execute( parser.prepareStatement( 
            parser.StatementType.DELETE, ["id", "due_date"], [id,date] ) )
        self.connection.commit()
        self.connection.close()
        print( "Succesfully deleted" )

class CommandLineParser( ArgumentParser ):

    def add_ls_subparser( self ):
        ls = self.subparsers.add_parser( 'ls', help="Lists tasks" )
        ls.add_argument( "-t", "--task", help="Task Name" )
        ls.add_argument( "-d", "--date", help="Due date of task" )

    def add_add_subparser( self ):
        add = self.subparsers.add_parser( 'add', help="Adds a task" )
        add.add_argument( "-t", "--task", required=True, help="Task Name" )
        add.add_argument( "-d", "--date", help="Due date of task" )

    def add_remove_subparser( self ):
        remove = self.subparsers.add_parser( 'remove', help="Removes a task" )
        remove.add_argument( "-i", "--id", required=True, help="Task ID" )

    def add_subparsers( self ):
        self.add_ls_subparser()
        self.add_remove_subparser()
        self.add_add_subparser()

    def __init__( self ):
        super().__init__()
        self.subparsers = super().add_subparsers( help="List of commands", dest="cmd" )
        self.subparsers._parser_class = ArgumentParser
        self.add_subparsers()

def main():
    parser = CommandLineParser()
    args = parser.parse_args()
    print( args )

    if( args.cmd == "add" ):
        CommandLineAPI().add( args.task, args.date )
    elif( args.cmd == "ls" ):
        CommandLineAPI().ls( args.task, args.date )
    else:
        CommandLineAPI().remove( args.id )

main()