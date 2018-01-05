#!/usr/local/bin/python3

class Constants:
    CMD_PARAMS = [ "-t", "-d", "-i" ]
    COMPARATORS = [ "-lt", "-le", "-gt", "-ge", "-eq", "-ne" ]
    CMDS = [ "add", "ls", "del", "upd" ]

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

def parse_text_param( args, i ):
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
    return text_param, i

def parse_numeric_param( args, i ):

    numeric_param = NumericParameter( None, None )

    while i < len(args) and args[i] not in Constants.CMD_PARAMS:
        if args[i] in Constants.COMPARATORS:
            numeric_param.comparator = args[i]
        else:
            numeric_param.value = args[i];
        
        i += 1
    i -= 1
    return numeric_param, i

def parse( args ):

    if len( args ) < 2:
        raise Exception( "Please specify a valid command from the following: add, ls, del, upd" )
        
    cmd = Command( args[1] )
    index = 2
    while index < len( args ):
        s = args[index]
        if s in Constants.CMD_PARAMS:
            index += 1
            if s == "-t":
                (task_name, i) = parse_text_param( args, index )
                cmd.task_name = task_name
            elif s == "-d":
                (task_date, i) = parse_numeric_param( args, index )
                cmd.task_date = task_date
            elif s == "-i":
                (task_index, i) = parse_numeric_param( args, index )
                cmd.task_index = task_index
            index = i
        index += 1

    return cmd 