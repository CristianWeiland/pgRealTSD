angular.module('DSMPN', ['ngResource', 'ui.router',
                         'ui.bootstrap', 'ngAnimate'])
    .config(function($stateProvider, $urlRouterProvider, $httpProvider) {
        $httpProvider.defaults.useXDomain = true;
        $urlRouterProvider.otherwise("/");
    })

	.config(['$qProvider', function ($qProvider) {
		$qProvider.errorOnUnhandledRejections(false);
	}])

    .factory('DataFactory', function() {
        return {
            data: {
                serverName: '',
                collectedAttrs: []
            }
        };
    })

    .controller('ContentCtrl',function($scope, $http, $alert, ServersFactory, DataFactory) {
        $scope.sharedData = DataFactory.data;
        $scope.interval = [];
		const interval = 10000; // Interval to get new data for our graph;
        const reqRefreshTime = 1; // How many minutes of data we should ask from server when we refresh;
        const reqInitialTime = 3; // How many minutes of data we should ask from server when initializing;

        function splitDate(date) {
            // Date is in following format: "DD/MM/YYYY HH:MM:SS";
            // tmp stores: ["DD/MM/YYYY", "HH:MM:SS"];
            var tmp = date.split(' ');
            // bigs stores: ["DD", "MM", "YYYY"];
            var bigs = tmp[0].split('/');
            // smalls stores: ["HH", "MM", "SS"];
            var smalls = tmp[1].split(':');

            return {
                day: bigs[0],
                month: bigs[1],
                year: bigs[2],
                hour: smalls[0],
                minute: smalls[1],
                second: smalls[2]
            };
        }

        function dateToSecEpoch(dateStr) {
            // Receives a date and returns seconds (or milisseconds, not sure) passed since epoch.
            var dateObj = splitDate(dateStr);
            // new Date has months starting in 0, so we have to use month-1.
            return new Date(dateObj.year, parseInt(dateObj.month, 10)-1, dateObj.day,
                            dateObj.hour, dateObj.minute, dateObj.second).getTime();
        }

        function reverseArray(array) {
            var result = [];
            var i = null;
            for (i = array.length - 1; i >= 0; i -= 1) {
                result.push(array[i]);
            }
            return result;
        }

        function refreshData(index, series, serverName, attr) {
            ServersFactory.getServerAttrPer(serverName, attr, '1', function(res) {
                // Reverse array, so the newest element will be in position 0.
                // A little bit faster than array.reverse()...
                var data = reverseArray(res.data.results);
                var idx = 0;
                // Fix date as number of ms passed since epoch.
                data.forEach(function(tuple) {
                    tuple.date = dateToSecEpoch(tuple.date);
                });

                var globalData = $scope.graphs[index].config.series[0].data;
                if (globalData.length > 0) {
                    // Acha o ultimo cara que eu inseri.
                    while (idx < data.length && data[idx].date !== globalData[globalData.length-1].x) {
                        ++idx;
                    }
                    --idx;
                } else {
                    idx = data.length - 1;
                }

                // Insere todos os dados novos. Se nao tiver dados novos, idx ja vale -1.
                while (idx > 0) {
                    $scope.graphs[index].chart.series[0].addPoint([ data[idx].date, data[idx].value ], false, true);
                    --idx;
                }
                $scope.graphs[index].chart.redraw();

            }, function(err) {
                console.log(err);
            });
        }

        function initializeServerData(idx, serverName, attr, graphs) {
            graphs[idx].attr = attr;
            ServersFactory.getServerAttrPer(serverName, attr, '1', function(res) {
                // res.data.results === [ { date: 11/11/11 11:11:11, value: 3123123 }, {}, ... ]
                for(var i=0; i<res.data.results.length; ++i) {
                    res.data.results[i].x = dateToSecEpoch(res.data.results[i].date);
                    res.data.results[i].y = res.data.results[i].value;
                }

                graphs[idx].config = {
                    chart: {
                        borderWidth: 1,
                        borderColor: '#C3C3C3',
                        type: 'spline',
                        animation: Highcharts.svg, // don't animate in old IE
                        marginRight: 10,
                    },
                    credits: false,
                    title: {
                        text: (attr) ? attr.charAt(0).toUpperCase() + attr.slice(1) : 'Unknown'
                    },
                    xAxis: {
                        title: {
                            text: 'Time'
                        },
                        type: 'datetime',
                        tickPixelInterval: 30
                    },
                    yAxis: {
                        title: {
                            text: (attr) ? attr.charAt(0).toUpperCase() + attr.slice(1) : 'Unknown'
                        },
                        plotLines: [{
                            value: 0,
                            width: 1,
                            color: '#808080'
                        }]
                    },
                    tooltip: {
                        formatter: function () {
                            return '<b>' + this.series.name + '</b><br/>Time: ' +
                                Highcharts.dateFormat('%Y-%m-%d %H:%M:%S', this.x) +
                                '<br/>Value: ' + this.y;
                        }
                    },
                    series: [{
                        name: 'Memória (KBs)',
                        data: res.data.results
                    }]
                };

                graphs[idx].chart = Highcharts.chart('container' + idx, graphs[idx].config); // Container é o id da div.
            });
        }

        $scope.$watch('sharedData.serverName', function(serverName) {
            if ($scope.interval) {
                clearInterval($scope.interval);
            }

            if (!serverName) return;


            if (!$scope.sharedData || !$scope.sharedData.collectedAttrs) return;

            console.log('Watching', serverName);
            $scope.graphs = [];

            for (var i=0; i<$scope.sharedData.collectedAttrs.length; ++i) {
                $scope.graphs.push({});
                var attr = $scope.sharedData.collectedAttrs[i].attribute;
                initializeServerData(i, serverName, attr, $scope.graphs);
            }

            setInterval(function() {
                for(var count=0; count<$scope.sharedData.collectedAttrs.length; ++count) {
                    var graph = $scope.graphs[count];
                    refreshData(count, graph.config.series[0], serverName, graph.attr);
                }
            }, interval);

            if ($scope.sharedData.collectedAttrs.length == 0) {
                $alert.error('Your server is not collecting any data. Please try again later.');
            }
        });
    })

    .factory('$alert', function ($rootScope) {
        function broadcastFactory(level) {
            return function (message) {
                $rootScope.$broadcast('$alert', {
                    level: level,
                    message: message
                });
            };
        }

        return {
            success: broadcastFactory('success'),
            debug:   broadcastFactory('debug'),
            info:    broadcastFactory('info'),
            warning: broadcastFactory('warning'),
            error:   broadcastFactory('error'),
            clear:   function (fadeTime) {
                $rootScope.$broadcast('$alertClear', fadeTime);
            }
        };
    })

	.directive('mcAlert', function () {
        return {
            restrict: 'AE',
            link: function (scope, element, attrs) {
                var alertTimeout;

                element.hide();
                element.addClass('alert alert-fixed');

                scope.$on('$alert', function (e, def) {
                    var msg;

                    element.removeClass('alert-success alert-info alert-warning alert-danger');

                    if (!def.level) {
                        console.error('undefined alert level');
                        return;
                    }

                    switch (def.level) {
                    case 'success':
                        element.addClass('alert-success');
                        msg = "<strong>Success!</strong> ";
                        break;
                    case 'debug':
                    case 'info':
                        element.addClass('alert-info');
                        msg = "";
                        break;
                    case 'warning':
                        element.addClass('alert-warning');
                        msg = "<strong>Warning!</strong> ";
                        break;
                    case 'error':
                        element.addClass('alert-danger');
                        msg = "<strong>Error!</strong> ";
                        break;
                    default:
                        console.error('unknown alert level');
                        return;
                        break;
                    }

                    msg += def.message || "Ocorreu um erro, tente novamente mais tarde.";

                    element.html(msg);
                    element.fadeIn(400);

                    if (alertTimeout)
                        clearTimeout(alertTimeout);

                    var timeout = def.timeout || 10*1000;

                    alertTimeout = setTimeout(function () {
                        element.fadeOut(500);
                    }, timeout);

                    element.click(function () {
                        element.fadeOut(500);
                    });
                });

                scope.$on('$alertClear', function (e, fadeTime) {
                    if (alertTimeout)
                        clearTimeout(alertTimeout);

                    element.fadeOut(fadeTime || 100);
                });
            }
        }
    })

    .factory('ServersFactory', function($http, $state) {
        return {
            addServer: function (server, username, successCallback, errorCallback) {
                if (!username || !server) {
                    console.log('(addServer) Server or username not specified. Aborting request...');
                    return;
                }

                $http({ url: 'http://localhost:8000/servers/new',
                        method: 'POST',
                        data: { name: server, user_name: username },
                        headers: {
                            'Content-Type': 'application/json; charset=utf-8'
                        } })
                    .then(function(res) {
                        if (successCallback) {
                            successCallback(res);
                        }
                    }, function(res) {
                        if (errorCallback) {
                            errorCallback(res);
                        }
                    }
                )
            },
            getServer: function (serverName, successCallback, errorCallback) {
                if (!serverName) {
                    console.log('(getServer) Server not specified. Aborting request...');
                    return;
                }

                $http({ url: 'http://localhost:8000/servers/' + serverName + '/',
                        method: 'GET' })
                    .then(function(data) {
                        if (successCallback) {
                            successCallback(data);
                        }
                    }, function(data) {
                        if (errorCallback) {
                            errorCallback(data);
                        }
                    }
                )
            },
            getAllServers: function (successCallback, errorCallback) {
                $http({ url: 'http://localhost:8000/servers/',
                        method: 'GET' })
                    .then(function(data) {
                        if (successCallback) {
                            successCallback(data);
                        }
                    }, function(data) {
                        if (errorCallback) {
                            errorCallback(data);
                        }
                    }
                )
            },
            getServersSorted: function (order, successCallback, errorCallback) {
                if (!order) {
                    console.log('(getServersSorted) Order not specified. Aborting request...');
                    return;
                }

                $http({ url: 'http://localhost:8000/server/order/',
                        params: { order: order },
                        method: 'GET' })
                    .then(function(data) {
                        if (successCallback) {
                            successCallback(data);
                        }
                    }, function(data) {
                        if (errorCallback) {
                            errorCallback(data);
                        }
                    }
                )
            },
            getServerAttrPer: function (server, attr, period, successCallback, errorCallback) {
                if (!attr || !server || !period) {
                    console.log('(getServerAttrPer) Attr, server or period not specified. Aborting request...');
                    return;
                }

                $http({ url: 'http://localhost:8000/servers/' + server + '/' + attr + '/' + period,
                        method: 'GET' })
                    .then(function(data) {
                        if (successCallback) {
                            successCallback(data, server, attr, period);
                        }
                    }, function(data) {
                        if (errorCallback) {
                            errorCallback(data);
                        }
                    }
                )
            },
            activateServer: function (server, successCallback, errorCallback) {
                if (!server) {
                    console.log('(activateServer) Server not specified. Aborting request...');
                    return;
                }

                $http({ url: 'http://localhost:8000/servers/' + server + '/activation',
                        method: 'PUT' })
                    .then(function(data) {
                        if (successCallback) {
                            successCallback(data);
                        }
                    }, function(data) {
                        if (errorCallback) {
                            errorCallback(data);
                        }
                    }
                )
            },
            deleteServer: function (server, successCallback, errorCallback) {
                if (!server) {
                    console.log('(deleteServer) Server not specified. Aborting request...');
                    return;
                }

                $http({ url: 'http://localhost:8000/servers/' + server + '/',
                        method: 'DELETE' })
                    .then(function(data) {
                        if (successCallback) {
                            successCallback(data);
                        }
                    }, function(data) {
                        if (errorCallback) {
                            errorCallback(data);
                        }
                    }
                )
            }
        }
    })

    .controller('MainCtrl', function($scope, $location, $timeout, $uibModal, $alert, $interval, ServersFactory, DataFactory) {
        var url = $location.url();

        $scope.changePage = function() {
            if ($scope.configPage && $scope.servers && $scope.servers.length == 0) {
                return;
            }
            $scope.configPage = !$scope.configPage;
        }

        $scope.sharedData = DataFactory.data;

        $scope.getIcon = (status) => {
            let icon = '';
            if(status === 'warmup') icon = 'plane';
            if(status === 'steady') icon = 'thumbs-up';
            if(status === 'under_pressure') icon = 'scale';
            if(status === 'stress') icon = 'warning-sign';
            if(status === 'trashing') icon = 'trash';
            return 'glyphicon-' + icon;
        }

        $scope.icons = {
            'warmup': 'glyphicon-plane',
            'steady': 'glyphicon-thumbs-up',
            'under_pressure': 'glyphicon-scale',
            'stress': 'glyphicon-warning-sign',
            'trashing': 'glyphicon-trash'
        }

        $scope.status_tip = (status) => {
            if(status === 'warmup') return 'Server is initializing...';
            if(status === 'steady') return 'Server is steady! Nice!';
            if(status === 'under_pressure') return 'Server is getting under pressure... Keep an eye on it!';
            if(status === 'stress') return 'Server is stressed! Please do something!';
            if(status === 'trashing') return 'Server is going to die. You have failed this city!';
        }

        $scope.servers = [];
        $scope.preventFirst = true;
        $scope.$watch('servers.length', function(val) {
            if ($scope.preventFirst) {
                $scope.preventFirst = false;
                return;
            }
            if (val === 0) {
                $scope.configPage = true;
            }
        });

		$scope.filteredServers = $scope.servers;
        $scope.props = { filter: '', empty: false };

        $scope.applyFilter = function() {
			if(!$scope.servers) return;
			if(!$scope.props.filter) {
				$scope.filteredServers = $scope.servers;
				return;
			}
			$scope.filteredServers = $scope.servers.filter(function(server) {
                return server.name.toLowerCase().indexOf($scope.props.filter.toLowerCase()) !== -1 ||
                       server.status.toLowerCase().indexOf($scope.props.filter.toLowerCase()) !== -1;
			});
        }

        $scope.selectServer = function(index) {
	        $scope.selected = $scope.filteredServers[index];
            ServersFactory.getServer($scope.selected.name, function(res) {
                // Obs: We can not change collectedAttrs reference, since it would break ng-repeat.
                $scope.sharedData.collectedAttrs = res.data.data_list;
                $scope.sharedData.data = res.data.data;
                $scope.sharedData.active = res.data.active;
                $scope.sharedData.state = res.data.state;
                // WARNING: Server name is the LAST attribute to be set in this function. DO NOT change this.
                // Thats because we watch over Server name, so it might run the watcher with undefined values.
                $scope.sharedData.serverName = res.data.name;
            });
        }

        // Initialization: Retrieve data from all servers..
        ServersFactory.getAllServers(function(res) {
            res.data.results.forEach(function(newServer) {
                $scope.filteredServers.push({
                    name: newServer.name,
                    status: newServer.state,
                    active: newServer.active,
                });
            });
            if (!$scope.selected && $scope.filteredServers && $scope.filteredServers.length > 0) {
                $scope.selectServer(0);
            } else {
                $scope.props.empty = true;
            }
        }, function(data) {
            $alert.error('Error getting all servers...');
        });

        // Begin config page functions.
        $scope.addServer = function(scope) {
			var modalInstance = $uibModal.open({
				animation: true,
				templateUrl: 'partials/new.server.modal.html',
                controller: function ($scope, $uibModalInstance, $state, $alert) {
					$scope.server = { name: '', status: '' };

					$scope.submit = function() {
						if(!$scope.server.name || !$scope.server.username) {
							$alert.error('Please fill the server name and current status.');
							return;
						}

                        ServersFactory.addServer($scope.server.name, $scope.server.username, function(data) {
                            $alert.success('Success adding server!');
    						scope.servers.push({ name: $scope.server.name, status: 'red', active: false });
                            scope.props.empty = false;
                        }, function(response) {
                            if (response.status === 422) {
                                $alert.error('Server already exists!');
                            } else {
                                $alert.error('Internal server error.');
                            }
                        });

                        $uibModalInstance.close();
					};

					$scope.cancel = function() {
                        $uibModalInstance.dismiss('cancel');
                    };

				}
            });
        };

        $scope.turn = function(server) {
            // Alert will be the opposite of server.active, so this is correct! DONT! TOUCH! IT!
            var power = server.active ? 'off' : 'on';
            ServersFactory.activateServer(server.name, function(res) {
                server.active = !server.active;
                $alert.success('Server \'' + server.name + '\' turned ' + power + '!');
            }, function() {
                $alert.error('Could not turn server \'' + server.name + '\' ' + power + '.');
            });
        }

        $scope.removeServer = function(server) {
            $scope.servers.splice($scope.servers.indexOf(server), 1);
            ServersFactory.deleteServer(server.name, function() {
                $alert.success('Server \'' + server.name + '\' successfully removed!');
            }, function() {
                $alert.error('Could not remove server \'' + server.name + '\'.');
            });
        }
        // End config page functions.
    })
