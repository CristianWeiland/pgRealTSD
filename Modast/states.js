const stateIdx = {
    warmup: 0,
    steady: 1,
    under_pressure: 2,
    stress: 3,
    thrashing: 4,
}

const states: ['warmup', 'steady', 'under_pressure', 'stress', 'thrashing']

const WARMUP_THRESHOLD: 0.1;
const STEADY_THRESHOLD: 0.9;
const STRESS_THRESHOLD: 0.1;
const THRASHING_THRESHOLD: 1.0;

module.exports = {
    getNextState: function(currentState, performanceVariation, transactionThroughput, performanceTrend, transactionsTreated) {
        if (currentState === states[0]) { // treat warmup
            return (performanceVariation < WARMUP_THRESHOLD) ? states[1] : states[0];

        } else if (currentState === states[1]) { // treat steady
            return (transactionThroughput > STEADY_THRESHOLD) ? states[1] : states[2];

        } else if (currentState === states[2]) { // treat under_pressure
            if (performanceVariation > STRESS_THRESHOLD * transactionsTreated) return states[3];
            if (transactionThroughput > STEADY_THRESHOLD) return states[1];
            return states[2];

        } else if (currentState === states[3]) { // treat stress
			if(performanceTrend < THRASHING_THRESHOLD * transactionThroughput) return states[4];
			if(performanceVariation <= STRESS_THRESHOLD) return states[2];
			return ModastStateEnum.STRESS_STATE;

        } else if (currentState === states[4]) { // treat trashing
			return states[4];
        }
		return currentState;
    },
    stateIdx: stateIdx,
	states: states,
};

