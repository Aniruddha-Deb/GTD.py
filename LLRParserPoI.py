#!/usr/local/bin/python3

import sys

class TextParameter( object ):

    def __init__( self, value, regexp, like ):
        self.value = value
        self.regexp = regexp
        self.like = like

    def __str__( self ):
        return "{}( regexp={}, like={} )".format( self.value, self.regexp, self.like )

class NumericParameter( object ):

    def __init__( self, value, comparator ):
        self.value = value
        self.comparator = comparator

    def __str__( self ):
        return "{}( comparator={} )".format( self.value, self.comparator )

def parse_text_param( args, i ):
    cmd_params = [ "-t", "-d", "-i" ]
    text_param = TextParameter( None, False, False )

    while i < len(args) and args[i] not in cmd_params:
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

    cmd_params = [ "-t", "-d", "-i" ]
    comparators = [ "-lt", "-le", "-gt", "-ge", "-eq", "-ne" ]
    numeric_param = NumericParameter( None, None )

    while i < len(args) and args[i] not in cmd_params:
        if args[i] in comparators:
            numeric_param.comparator = args[i]
        else:
            numeric_param.value = args[i];
        
        i += 1
    i -= 1
    return numeric_param, i

def main( args=sys.argv ):

    params = [ "-t", "-d", "-i" ]

    index = 0
    while index < len( args ):
        s = args[index]
        if s in params:
            index += 1
            if s == "-t":
                (task_name, i) = parse_text_param( args, index )
                print( task_name )
            elif s == "-d":
                (task_date, i) = parse_numeric_param( args, index )
                print( task_date )
            elif s == "-i":
                (task_index, i) = parse_numeric_param( args, index )
                print( task_index )
            index = i
        index += 1
main()