let splitDate = (date) => {
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

export default {
    capitalize(str) {
        if (!str || !str[0]) return '';
        return str.charAt(0).toUpperCase() + str.slice(1);
    },
    splitDate: splitDate,

    dateToSecEpoch: (dateStr) => {
        // Receives a date and returns seconds (or milisseconds, not sure) passed since epoch.
        var dateObj = splitDate(dateStr);
        // new Date has months starting in 0, so we have to use month-1.
        return new Date(dateObj.year, parseInt(dateObj.month, 10)-1, dateObj.day,
                        dateObj.hour, dateObj.minute, dateObj.second).getTime();
    },

    reverseArray: (array) => {
        var result = [];
        var i = null;
        for (i = array.length - 1; i >= 0; i -= 1) {
            result.push(array[i]);
        }
        return result;
    },
    /*
    refreshData: (index, series, serverName, attr) => {
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
    },
    */
};
