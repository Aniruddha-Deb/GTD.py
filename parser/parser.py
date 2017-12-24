#!/usr/local/bin/python3

from enum import Enum

class TokenType( Enum ):
    STRING = 1
    RELATIONAL_OP = 2
    LITERAL = 3

class StatementType( Enum ):
    INSERT = 1
    SELECT = 2
    DELETE = 3

class Token( object ):

    def __init__( self, value, type ):
        self.value = value
        self.type = type

    def __str__( self ):
        return str( self.value + " : " + str( self.type ) )

    def __repr__( self ):
        return str( self.value + " : " + str( self.type ) )

def tokenize( string ):

    if string == None:
        return None

    tokens = []
    relational_operators = { ">", "<", "=" }
    reserved_chars = { ">", "<", "=" }
    x = list( string )
    i=0
    currStr = ""
    while i < len(x):
        char = x[i]
        if any( char in y for y in reserved_chars ):
            rel_tok = char
            if any( x[i+1] in z for z in relational_operators ):
                rel_tok += x[i+1]
                i += 1
            tokens.append( Token( rel_tok, TokenType.RELATIONAL_OP ) )

        elif char.isdigit() or char == '.':
            rel_tok = char
            i += 1
            isString = False
            while i < len(x) and (x[i].isdigit() or x[i] == '.'):
                if x[i] == '.':
                    isString = True
                rel_tok += x[i]
                i += 1
            i -= 1
            if isString:
                tokens.append( Token( rel_tok, TokenType.STRING ) )
            else:
                tokens.append( Token( rel_tok, TokenType.LITERAL ) )
        i += 1
    return tokens

def prepareStatement( statement_type, params, tokens ):
    stmt = ""
    if statement_type == StatementType.SELECT:
        stmt = "SELECT * FROM tasks"
    elif statement_type == StatementType.DELETE:
        stmt = "DELETE FROM tasks"

    num_none = 0
    for t in tokens:
        if t == None:
            num_none += 1

    if not num_none == len(tokens) :
        stmt += " WHERE "
        i=0
        added=False
        for p in params:
            curr_token = tokenize( tokens[i] )
            if not curr_token == None:
                if not i == 0 and added == True:
                    stmt += " AND "
                stmt += p
                if curr_token[0].type == TokenType.RELATIONAL_OP:
                    stmt += curr_token[0].value
                    if curr_token[1].type == TokenType.LITERAL:
                        stmt += curr_token[1].value
                    elif curr_token[1].type == TokenType.STRING:
                        stmt += "\"" + curr_token[1].value + "\""
                elif curr_token[0].type == TokenType.LITERAL:
                    stmt += "=" + curr_token[0].value
                added=True
            i += 1
    return stmt
