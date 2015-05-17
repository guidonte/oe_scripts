#! /usr/bin/python

import argparse


def oe_args_parser():
    parser = argparse.ArgumentParser()

    parser.add_argument('-d', '--database', dest='database', required=True)
    parser.add_argument('-u', '--username', dest='username', default='admin')
    parser.add_argument('-p', '--password', dest='password')
    parser.add_argument('-h', '--host', dest='host', default='localhost')
    parser.add_argument('-P', '--port', dest='port', default='8069')

    return parser

def oe_parse_args(args):
    parser = oe_args_parser()

    return parser.parse_args(args)
