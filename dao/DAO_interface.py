#!/usr/local/bin/python3

class DAOInterface( object ):

    def __init__( self ):
        print( "Init " )

    def create_task( self, task ):
        raise NotImplementedError( "Should implement create_task" )

    def read_task( self, task ):
        raise NotImplementedError( "Should implement read_task" )

    def update_task( self, task ):
        raise NotImplementedError( "Should implement update_task" )        

    def delete_task( self, task ):
        raise NotImplementedError( "Should implement delete_task" )
