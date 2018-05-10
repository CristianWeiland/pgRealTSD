// require { calculatePerformanceVariation, calculateTransactionTroughput, calculatePerformanceTrend } from './performanceInputsCalculator.js';
var calculator = require('./performanceInputsCalculator.js');
var stateMachine = require('./states.js');

console.log('Initializing Modast...');
console.log('');

function validateData(data) {
    // Try-catch block makes sure nTransactionsTreated / Requested props exist
    try {
        if (data.nTransactionsTreated.length !== data.nTransactionsRequested.length
         || data.timestamps.length !== data.nTransactionsTreated.length) {
            return false;
        }
        let sum1 = data.nTransactionsTreated.reduce((a, b) => a + b, 0);
        let sum2 = data.nTransactionsTreated.reduce((a, b) => a + b, 0);
        // Cant answer more than we requested.. Or can we? Maybe if there are other requests already being processed...
        if (sum2 > sum1) return false;

        return true;
    } catch(e) {
        return false;
    }
}

const iteration = 5; // what the fuck is this
const nTransactionsTreated = [1.1, 1.3, 1.5, 1.9, 10.2, 0.3, 0.5];
const windowSize = 5;

const data1 = {
    nTransactionsTreated: [5, 7, 10, 2, 3, 1],
    nTransactionsRequested: [10, 10, 5, 2, 1, 0],
    timestamps: [
        1524318526,
        1524318527,
        1524318528,
        1524318529,
        1524318530,
        1524318531
    ]
};

// Check data consistency:
let data = data1;

if (!validateData(data)) {
    console.log('[WARN] Data looks invalid... check it out!');
}

console.log('Value is ' + calculator.calculatePerformanceVariation(iteration, data.nTransactionsTreated, windowSize));
console.log('');


console.log('Stopping Modast');

