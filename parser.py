#!/usr/local/bin/python3

from datetime import datetime, timedelta

class Parser( object ): 

    def parse( self, args ):
        parameter_parsers = { "-t":self.parse_task_param, 
                              "-d":self.parse_date_param,
                              "-i":self.parse_id_param }
        cmd = Command( args[1] )
        index = 2
        while index < len( args ):
            s = args[index]
            if s in Constants.CMD_PARAMS:
                index += 1
                index = parameter_parsers[s]( args, index, cmd )
            index += 1
        return cmd 

    def parse_task_param( self, args, i, cmd ):
        like = regexp = False
        value = None

        while i < len(args) and args[i] not in Constants.CMD_PARAMS:
            if args[i] == "-r":
                regexp = True
            elif args[i] == "-l":
                like = True
            else:
                value = args[i]
            
            i += 1
        i -= 1
        cmd.task_name = TextParameter( value, regexp, like )
        return i

    def parse_numeric_param( self, args, i ):

        comparator = value = None

        while i < len(args) and args[i] not in Constants.CMD_PARAMS:
            if args[i] in Constants.COMPARATORS:
                comparator = args[i]
            else:
                value = args[i];

            i += 1
        i -= 1
        return ( NumericParameter( value, comparator ), i )

    def parse_date_param( self, args, i, cmd ):
        (numeric_param, i) = self.parse_numeric_param( args, i )
        cmd.task_date = numeric_param
        return i

    def parse_id_param( self, args, i, cmd ):
        (numeric_param, i) = self.parse_numeric_param( args, i )
        cmd.task_index = numeric_param
        return i

    def process_date( self, date ):
        today = datetime.now().date()
        if date == None or date.value == None:
            return today.strftime( "%d.%m.%Y" )
        elif date.value.startswith( "t" ):
            if len( date.value ) > 2:
                numDays = int( date.value[2:] )
                today = eval( "today " + date.value[1] + "timedelta({})".format( numDays ) )
            return today.strftime( "%d.%m.%Y" )
        else:
            return date


class AddParser( Parser ):

    def parse( self, args ):
        print( "AddParser" )
        cmd = super().parse( args )
        if cmd.task_name == None:
            raise Exception( "Add command requires a task name" )
        cmd.task_date.value = super().process_date( cmd.task_date )
        return cmd

class ListParser( Parser ):
    def parse( self, args ):
        return super().parse( args )

class DeleteParser( Parser ):
    def parse( self, args ):
        return super().parse( args )

class UpdateParser( Parser ):
    def parse( self, args ):
        cmd = super().parse( args )
        if cmd.task_id == None:
            raise Exception( "Update command requires a task ID" )
        return cmd

class Constants:
    CMD_PARAMS = [ "-t", "-d", "-i" ]
    COMPARATORS = [ "-lt", "-le", "-gt", "-ge", "-eq", "-ne" ]
    CMDS = [ "add", "ls", "del", "upd", "today" ]

class Command( object ):

    def __init__( self, name ):
        self.name = name
        self.task_name = None
        self.task_date = None
        self.task_index = None

    def __str__( self ):
        return "{}:\n\tName: {}\n\tDate: {}\n\tID: {}".format( 
            self.name, self.task_name, self.task_date, self.task_index )

class Parameter( object ):
    
    def __init__( self, value ):
        self.value = value
        if value == None:
            raise Exception( "Parameter requires a value" )

class TextParameter( Parameter ):

    def __init__( self, value, regexp, like ):
        super().__init__( value )
        self.regexp = regexp
        self.like = like

    def __str__( self ):
        return "{}( regexp={}, like={} )".format( self.value, self.regexp, self.like )

class NumericParameter( Parameter ):

    def __init__( self, value, comparator ):
        super().__init__( value )
        self.comparator = comparator

    def __str__( self ):
        return "{}( comparator={} )".format( self.value, self.comparator )

cmds = { "add": AddParser,
         "ls" : ListParser,
         "del": DeleteParser,
         "upd": UpdateParser }

def parse( args ):

    if len( args ) < 2:
        return Command( "today" )

    parser = cmds[args[1]]()
    return parser.parse( args )