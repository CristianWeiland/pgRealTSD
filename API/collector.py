# -*- coding=utf-8 -*-

from subprocess import Popen, PIPE
from optparse import OptionParser
from re import sub
from getpass import getuser
from MoDaST import variables, states

import json
import time
import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "Backend.settings")
django.setup()

from service.models import Data, DataList, Server
from service.serializers import DataSerializer

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

    timestamp_now = int( time.time() )
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

    server = Server.objects.get(name=arguments.server_name)

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

    for key, value in requests.items():
        try:
            data = Data.objects.get(timestamp=int(key), data_list=data_list_request)
            data.value += value
            data.save()
        except:
            data = Data()
            data.data_list = data_list_request
            data.value = value
            data.timestamp = key
            data.save()
    
    for key, value in responses.items():
        try:
            data = Data.objects.get(timestamp=int(key), data_list=data_list_response)
            data.value += value
            data.save()
        except:
            data = Data()
            data.data_list = data_list_response
            data.value = value
            data.timestamp = key
            data.save()


def get_states_data(time_now, window_size):
    requests = Data.objects.filter(timestamp__gte = time_now - window_size, timestamp__lte = time_now, data_list__attribute = 'requests').order_by('timestamp')
    responses = Data.objects.filter(timestamp__gte = time_now - window_size, timestamp__lte = time_now, data_list__attribute = 'responses').order_by('timestamp')

    timestamp_list = []
    requests_list = []
    responses_list = []
    for timestamp in range((time_now - window_size), time_now):
        try:
            request = DataSerializer(requests.get(timestamp=timestamp)).data.get('value')
        except:
            request = None
        try:
            response = DataSerializer(responses.get(timestamp=timestamp)).data.get('value')
        except:
            response = None
        if request and response:
            timestamp_list.append(timestamp)
            requests_list.append(request)
            responses_list.append(response)

    return timestamp_list, requests_list, responses_list

# Start program
arguments = read_arguments()

requests_data_refresh(arguments)

try:
    server = Server.objects.get(name=arguments.server_name)
except:
    server = Server()
    server.name = arguments.server_name
    server.user_name = arguments.user_name
    server.save()

    print('Server ' + server.name + ' added to database.')

try:
    data_list_state = DataList.objects.get(attribute='states', server=server)
except:
    data_list_state = DataList()
    data_list_state.attribute = 'states'
    data_list_state.server = server
    data_list_state.save()

while True:
    output = get_attributes(arguments)
    requests_time_data = get_requests_time(arguments)

    requests = {}
    responses = {}
    for line in requests_time_data.split('\n')[1: (len(requests_time_data.split('\n')) - 1)]:
        attributes = line.split(' ')
        if (int(attributes[3]) < 300):
            if requests.get(str(int(float(attributes[1]) - float(attributes[2])))):
                requests[str(int(float(attributes[1]) - float(attributes[2])))] +=1
            else:
                requests[str(int(float(attributes[1]) - float(attributes[2])))] = 1

            if responses.get(str(int(float(attributes[1])))):
                responses[str(int(float(attributes[1])))] += 1
            else:
                responses[str(int(float(attributes[1])))] = 1
        else:
            if requests.get(str(int(float(attributes[1])))):
                requests[str(int(float(attributes[1])))] += 1
            else:
                requests[str(int(float(attributes[1])))] = 1

    attributes_names_list = output.splitlines()[1].split()
    attributes_values_list = output.splitlines()[2].split()

    save_attributes(attributes_names_list, attributes_values_list, arguments)
    save_requests_time(requests, responses, arguments)

    window_size = 60
    time_now = int(time.time())

    states_query = Data.objects.filter(timestamp__gte = time_now - window_size, timestamp__lte = time_now, data_list__attribute = 'states').order_by('-timestamp')
    if len(states_query) != 0:
        last_state_timestamp = states_query[0].timestamp + 1
        last_state_value = states_query[0].value
    else:
        last_state_timestamp = time_now - window_size
        last_state_value = 1
    
    for timestamp in range(last_state_timestamp, time_now):
        timestamp_list, requests_list, responses_list = get_states_data(timestamp, window_size)

        if len(timestamp_list) > 0:
            performanceVariation = variables.calculatePerformanceVariation(len(timestamp_list), responses_list, window_size)
            transactionTroughput = variables.calculateTransactionTroughput(responses_list, requests_list, window_size)
            performanceTrend = variables.calculatePerformanceTrend(timestamp_list, responses_list, window_size)

            currentState = states.getNextState(last_state_value, performanceVariation, transactionTroughput, performanceTrend, responses_list[len(responses_list) - 1])
            print(str(performanceVariation) + ' | ' + str(transactionTroughput) + ' | ' + str(performanceTrend) + ' | ' + str(currentState))
            
            data = Data()
            data.data_list = data_list_state
            data.timestamp = timestamp
            data.value = currentState
            data.save()

    if arguments.verbose: print(attributes_values_list)

    # TODO: Descomentar isso para rodar a API
    # if not Server.objects.get(name=arguments.server_name).active: break
