module.exports = {
    /*
    Params:
    - (Int) iteration: what the fuck is this;
    - (Int array) nTransactionsTreated: Array of ints representing the number of treated transactions in that second;
    - (Int) windowSize: how many elements from nTransactionsTreated we will use to calculate the performanceVariation.
    */
    calculatePerformanceVariation: function( iteration, nTransactionsTreated, windowSize) {
        if ((iteration - 1) == 0) {
            return 0.0;
        }

        let micro = nTransactionsTreated.reduce((a, b) => {
            return a + b;
        }, 0.0);
        micro = micro / iteration;

        let len = nTransactionsTreated.length;
        let sum = 0.0;
        let i = (len - windowSize < 0) ? 0 : len - windowSize;
        for (; i < len; i += 1) {
            let x = nTransactionsTreated[i] - micro;
            sum += x * x;
        }

        let delta = Math.sqrt(sum / (iteration - 1));

        return delta;
    }

    /*
    Params:
    - (Int) nTransactionsTreated: Integer representing the number of treated transactions in one second;
    - (Int) nTransactionsRequested: Integer representing the number of requested transactions in the same second;
    */
    calculateTransactionTroughput: function (nTransactionsTreated, nTransactionsRequested) {
        if (transactionsRequestedAvg == 0) return 0.0;

        return nTransactionsTreated / nTransactionsRequested;
    }


    calculatePerformanceTrend function () {
        // TODO fix futuro
        return 0.0;
    }
};

