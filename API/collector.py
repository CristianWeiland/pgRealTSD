# -*- coding=utf-8 -*-

from subprocess import Popen, PIPE
from optparse import OptionParser
from re import sub
from getpass import getuser

import time
import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "Backend.settings")
django.setup()

from service.models import Data, DataList, Server

timestamp_now = 0

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
    global timestamp_now

    if arguments.password:
        stdout, stderr = Popen(['sshpass', '-p', arguments.password, 'ssh', '-o', 'StrictHostKeyChecking=no', arguments.user_name+'@'+arguments.server_name, 'vmstat'],
                               stdout=PIPE).communicate()
    else:
        stdout, stderr = Popen(['ssh', arguments.user_name+'@'+arguments.server_name, 'vmstat'],
                               stdout=PIPE).communicate()

    timestamp_now = int(time.time())
    output = stdout.decode("utf-8")

    return output


def requests_data_refresh(arguments):
    global timestamp_now

    if arguments.password:
        stdout, stderr = Popen(
            [
                'sshpass',
                '-p',
                arguments.password,
                'ssh',
                '-o',
                'StrictHostKeyChecking=no',
                arguments.user_name+'@'+arguments.server_name,
                'sudo cp /var/log/nginx/access.log /var/log/nginx/access.bkp.log'
            ],
            stdout=PIPE
        ).communicate()
    else:
        stdout, stderr = Popen(
            [
                'ssh',
                arguments.user_name+'@'+arguments.server_name,
                'sudo cp /var/log/nginx/access.log /var/log/nginx/access.bkp.log'
            ],
            stdout=PIPE
        ).communicate()

    output = stdout.decode("utf-8")


def get_requests_time(arguments):
    global timestamp_now

    if arguments.password:
        stdout, stderr = Popen(
            [
                'sshpass',
                '-p',
                arguments.password,
                'ssh',
                '-o',
                'StrictHostKeyChecking=no',
                arguments.user_name+'@'+arguments.server_name,
                'diff /var/log/nginx/access.log /var/log/nginx/access.bkp.log'
            ],
            stdout=PIPE
        ).communicate()

        requests_data_refresh(arguments)
    else:
        stdout, stderr = Popen(
            [
                'ssh',
                arguments.user_name+'@'+arguments.server_name,
                'diff /var/log/nginx/access.log /var/log/nginx/access.bkp.log'
            ],
            stdout=PIPE
        ).communicate()

        requests_data_refresh(arguments)

    output = stdout.decode("utf-8")

    return output


def save_attributes(attributes_names_list, attributes_values_list, arguments):
    global timestamp_now

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
            data_list = DataList.objects.get(attribute=attributes_names_list[i], server=server)
        except:
            data_list = DataList()
            data_list.attribute = attributes_names_list[i]
            data_list.server = server
            data_list.save()

        try:
            data = Data.objects.get(timestamp=timestamp_now, data_list=data_list)
            data.value = int(attributes_values_list[i])
            data.save()
        except:
            data = Data()
            data.data_list = data_list
            data.value = int(attributes_values_list[i])
            data.timestamp = timestamp_now
            data.save()


def save_requests_time(requests, responses, arguments):
    global timestamp_now

    try:
        server = Server.objects.get(name=arguments.server_name)
    except:
        server = Server()
        server.name = arguments.server_name
        server.user_name = arguments.user_name
        server.save()

        print('Server ' + server.name + ' added to database.')

    try:
        data_list_request = DataList.objects.get(attribute='requests', server=server)
    except:
        data_list_request = DataList()
        data_list_request.attribute = 'requests'
        data_list_request.server = server
        data_list_request.save()

    try:
        data_list_response = DataList.objects.get(attribute='responses', server=server)
    except:
        data_list_response = DataList()
        data_list_response.attribute = 'responses'
        data_list_response.server = server
        data_list_response.save()

    for request in requests:
        try:
            data = Data.objects.get(timestamp=request, data_list=data_list_request)
            data.value += 1
            data.save()
        except:
            data = Data()
            data.data_list = data_list_request
            data.value = 1
            data.timestamp = request
            data.save()
    
    for response in responses:
        try:
            data = Data.objects.get(timestamp=response, data_list=data_list_response)
            data.value += 1
            data.save()
        except:
            data = Data()
            data.data_list = data_list_response
            data.value = 1
            data.timestamp = response
            data.save()


# Start program
arguments = read_arguments()

requests_data_refresh(arguments)
while True:
    output = get_attributes(arguments)
    requests_time_data = get_requests_time(arguments)

    requests = []
    responses = []
    for line in requests_time_data.split('\n')[1: (len(requests_time_data.split('\n')) - 1)]:
        attributes = line.split(' ')
        if (int(attributes[3]) < 300):
            requests.append(
                int(float(attributes[1]) - float(attributes[2]))
            )
            responses.append(int(float(attributes[1])))
        else:
            requests.append(int(float(attributes[1])))

    attributes_names_list = output.splitlines()[1].split()
    attributes_values_list = output.splitlines()[2].split()

    save_attributes(attributes_names_list, attributes_values_list, arguments)
    save_requests_time(requests, responses, arguments)

    if arguments.verbose: print(attributes_values_list)
    if not Server.objects.get(name=arguments.server_name).active: break
