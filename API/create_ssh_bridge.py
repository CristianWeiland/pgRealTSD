# -*- coding=utf-8 -*-

from subprocess import Popen, PIPE
from optparse import OptionParser
from getpass import getuser
from pathlib import Path

import os

def read_arguments():
    parser = OptionParser()
    parser.add_option('-u', '--user', dest='user_name', default=getuser(),
    help='Username to make login with server. Default: %default')
    parser.add_option('-s', '--server', dest='server_name', default='localhost',
    help='Name of server. Default: %default')
    parser.add_option('-p', '--password', dest='password',
    help='Password to make login with server.')

    (options, args) = parser.parse_args()

    return options


def send_key(arguments):
    id_rsa_pub_file = open(os.path.expanduser('~/.ssh/id_rsa.pub'), 'r')
    key = id_rsa_pub_file.read()

    stdout, stderr = Popen(
        [
            'sshpass',
            '-p',
            arguments.password,
            'ssh',
            '-o',
            'StrictHostKeyChecking=no',
            arguments.user_name+'@'+arguments.server_name,
            'echo "'+ key + '" >> ~/.ssh/authorized_keys'
        ],
        stderr=PIPE
    ).communicate()

    if ('Permission' in stderr.decode("utf-8").split()) or ('Could' in stderr.decode("utf-8").split()):
        print('User, server or password wrong.', end='')

    else:
        print('ok', end='')


# Start program

arguments = read_arguments()
send_key(arguments)
