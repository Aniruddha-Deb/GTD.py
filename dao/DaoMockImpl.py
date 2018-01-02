#!/usr/local/bin/python3

from dao import DAO_interface

class DaoMockImpl( DAO_interface.DAOInterface ):
    """Mock impl"""

    def __init__( self ):
        super().__init__()

    def create_task( self, task ):
        print( "Implemented create_task" )