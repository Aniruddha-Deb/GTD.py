#!/usr/local/bin/python3

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

def parse_task_param( args, i, cmd ):
    text_param = TextParameter( None, False, False )

    while i < len(args) and args[i] not in Constants.CMD_PARAMS:
        if args[i] == "-r":
            text_param.regexp = True
        elif args[i] == "-l":
            text_param.like = True
        else:
            text_param.value = args[i]
        
        i += 1
    i -= 1
    cmd.task_name = text_param
    return i

def parse_numeric_param( args, i ):

    numeric_param = NumericParameter( None, None )

    while i < len(args) and args[i] not in Constants.CMD_PARAMS:
        if args[i] in Constants.COMPARATORS:
            numeric_param.comparator = args[i]
        else:
            numeric_param.value = args[i];
        
        i += 1
    i -= 1
    return (numeric_param, i)

def parse_date_param( args, i, cmd ):
    (numeric_param, i) = parse_numeric_param( args, i )
    cmd.task_date = numeric_param
    return i

def parse_id_param( args, i, cmd ):
    (numeric_param, i) = parse_numeric_param( args, i )
    cmd.task_id = numeric_param
    return i

parameter_parsers = { "-t":parse_task_param, 
                      "-d":parse_date_param,
                      "-i":parse_id_param }

def parse( args ):

    if len( args ) < 2:
        return Command( "today" )

    cmd = Command( args[1] )
    index = 2
    while index < len( args ):
        s = args[index]
        if s in Constants.CMD_PARAMS:
            index += 1
            index = parameter_parsers[s]( args, index, cmd )
        index += 1

    return cmd 