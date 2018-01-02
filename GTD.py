#!/usr/local/bin/python3

from dao import DaoMockImpl

def main():
    impl = DaoMockImpl.DaoMockImpl()
    impl.create_task( "Hello" )

main()