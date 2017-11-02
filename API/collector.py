# -*- coding=utf-8 -*-

from subprocess import Popen, PIPE
from optparse import OptionParser
from re import sub
from getpass import getuser

import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "Backend.settings")
django.setup()

from service.models import Data, DataList, Server


def read_arguments():
    parser = OptionParser()
    parser.add_option('-u', '--user', dest='user_name', default=getuser(),
    help='Username to make login with server. Default: %default')
    parser.add_option('-s', '--server', dest='server_name', default='localhost',
    help='Name of server. Default: %default')
    parser.add_option('-p', '--password', dest='password',
    help='Password to make login with server.')
    parser.add_option('-v', '--verbose',
    action="store_true", dest="verbose", default=False,
    help='Activate verbose mode.')

    (options, args) = parser.parse_args()

    return options


def get_attributes(arguments):

    if arguments.password:
        stdout, stderr = Popen(['sshpass', '-p', arguments.password, 'ssh', '-o', 'StrictHostKeyChecking=no', arguments.user_name+'@'+arguments.server_name, 'vmstat'],
                               stdout=PIPE).communicate()
    else:
        stdout, stderr = Popen(['ssh', arguments.user_name+'@'+arguments.server_name, 'vmstat'],
                               stdout=PIPE).communicate()

    output = stdout.decode("utf-8")

    return output


def save_attributes(attributes_names_list, attributes_values_list, arguments):
    try:
        Server.objects.get(name=arguments.server_name)
    except:
        new_server = Server()
        new_server.name = arguments.server_name
        new_server.user_name = arguments.user_name
        new_server.save()

        print('Server ' + new_server.name + ' added to database.')

    server = Server.objects.get(name=arguments.server_name)

    for i in range(len(attributes_names_list)):
        data = Data()

        try:
            DataList.objects.get(attribute=attributes_names_list[i], server=server)
        except:
            data_list = DataList()
            data_list.attribute = attributes_names_list[i]
            data_list.server = server
            data_list.save()

        data.data_list = DataList.objects.get(attribute=attributes_names_list[i], server=server)
        data.value = int(attributes_values_list[i])
        data.save()


# Start program

arguments = read_arguments()

while True:
    output = get_attributes(arguments)

    attributes_names_list = output.splitlines()[1].split()
    attributes_values_list = output.splitlines()[2].split()

    save_attributes(attributes_names_list, attributes_values_list, arguments)

    if arguments.verbose: print(attributes_values_list)
    if not Server.objects.get(name=arguments.server_name).active: break
