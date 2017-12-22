#!/usr/local/bin/python3

from enum import Enum

class TokenType( Enum ):
    WILDCARD = 1
    RELATIONAL_OP = 2
    LITERAL = 3

class Token( object ):

    def __init__( self, value, type ):
        self.value = value
        self.type = type

    def __str__( self ):
        return str( self.value + " : " + str( self.type ) )

    def __repr__( self ):
        return str( self.value + " : " + str( self.type ) )

def tokenize( string ):
    tokens = []
    relational_operators = { ">", "<", "=", "^" }
    reserved_chars = { ">", "<", "=", "*", "^" }
    x = list( string )
    i=0
    currStr = ""
    while i < len(x):
        char = x[i]
        if any( char in y for y in reserved_chars ):
            if char == "*":
                tokens.append( Token( char, TokenType.WILDCARD ) )

            elif any( char in y for y in relational_operators ):
                rel_tok = char
                if any( x[i+1] in z for z in relational_operators ):
                    rel_tok += x[i+1]
                    i += 1
                tokens.append( Token( rel_tok, TokenType.RELATIONAL_OP ) )

        elif not char.isspace() :
            rel_tok = char
            i += 1
            while i < len(x) and (not any( x[i] in y for y in reserved_chars )):
                if x[i] == "\\":
                    i += 1
                rel_tok += x[i]
                i += 1
            i -= 1
            tokens.append( Token( rel_tok, TokenType.LITERAL ) )
        i += 1
    return tokens

print( tokenize( "^=3" ) )