#!/usr/local/bin/python3

import sys

import parser
import DAO

cmd = parser.parse( args=sys.argv )
DAO.execute( cmd )
