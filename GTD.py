#!/usr/local/bin/python3

from argparse import ArgumentParser

class Task( object ):

    def __init__( self, name, date ):
        self.name = name
        self.date = date

class CommandLineParser( ArgumentParser ):

    def create_task_parser( self ):
        task = ArgumentParser()
        task.add_argument( "-t", "--task", action='store_true', required=True, help="Create task" )        
        group = task.add_mutually_exclusive_group()
        group.add_argument( "-r", "--regexp", help="regexp", action='store_true' )
        group.add_argument( "-l", "--like", help="like", action='store_true' )
        task.add_argument( "task", help="Help" )
        return task

    def create_date_parser( self ):
        date = ArgumentParser()
        date.add_argument( "-d", "--date", action='store_true', required=True, help="Create task" )
        group = date.add_mutually_exclusive_group()
        group.add_argument( "--lt", action='store_const', const="lt" )
        group.add_argument( "--le", action='store_const', const="le" )
        group.add_argument( "--gt", action='store_const', const="gt" )
        group.add_argument( "--ge", action='store_const', const="ge" )
        group.add_argument( "--eq", action='store_const', const="eq" )
        group.add_argument( "--ne", action='store_const', const="ne" )
        date.add_argument( "date", help="Help" )
        return date

    def create_id_parser( self ):
        id = ArgumentParser()
        id.add_argument( "-i", "--id", action='store_true', required=True, help="Create task" )
        group = id.add_mutually_exclusive_group()
        group.add_argument( "--lt", action='store_const', const="lt" )
        group.add_argument( "--le", action='store_const', const="le" )
        group.add_argument( "--gt", action='store_const', const="gt" )
        group.add_argument( "--ge", action='store_const', const="ge" )
        group.add_argument( "--eq", action='store_const', const="eq" )
        group.add_argument( "--ne", action='store_const', const="ne" )
        id.add_argument( "id", type=int, help="Help" )
        return id

    def create_add_subparser( self ):
        add = self.subparsers.add_parser( "add" )

    def create_ls_subparser( self ):
        ls = self.subparsers.add_parser( "ls" )

    def create_del_subparser( self ):
        delete = self.subparsers.add_parser( "del" )

    def create_upd_subparser( self ):
        upd = self.subparsers.add_parser( "upd" )

    def create_subparsers( self ):
        self.create_task_parser()
        self.create_add_subparser()
        self.create_ls_subparser()
        self.create_del_subparser()
        self.create_upd_subparser()

    def __init__( self ):
        super().__init__()
        self.subparsers = self.add_subparsers( help="List of commands", dest="cmd" )
        self.subparsers._parser_class = ArgumentParser
        self.create_subparsers()

    def parse_args( self ):
        (init_ns, remaining) = super().parse_known_args()
        print( init_ns )
        print( remaining )
        if remaining:
            (ns, rem) = self.create_task_parser().parse_known_args( args=remaining, namespace=init_ns )
            print( init_ns )
            print( rem )
            if rem:
                (n, r) = self.create_date_parser().parse_known_args( args=rem, namespace=ns )
                print( init_ns )
                print( r )
                if r:
                    self.create_id_parser().parse_known_args( args=r, namespace=n )
        return init_ns

parser = CommandLineParser()
args = parser.parse_args()
print( args )