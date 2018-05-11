states = ['warmup', 'steady', 'under_pressure', 'stress', 'thrashing']
initialState = 'warmup'

WARMUP_THRESHOLD = 0.1
STEADY_THRESHOLD = 0.9
STRESS_THRESHOLD = 0.1
THRASHING_THRESHOLD = 1.0

def getNextState(currentState, performanceVariation, transactionTroughput, performanceTrend, transactionsTreated):
    if currentState == states[0]: # treat warmup
        if performanceVariation < WARMUP_THRESHOLD:
            return states[1]
        return states[0]

    elif currentState == states[1]: # treat steady
        if transactionTroughput > STEADY_THRESHOLD:
            return states[1]
        return states[2]

    elif currentState == states[2]: # treat under_pressure
        if performanceVariation > STRESS_THRESHOLD * transactionsTreated:
            return states[3]
        if transactionTroughput > STEADY_THRESHOLD:
            return states[1]
        return states[2]

    elif currentState == states[3]: # treat stress
        if performanceTrend is not None and performanceTrend < (THRASHING_THRESHOLD * transactionTroughput):
            return states[4]
        if performanceVariation <= STRESS_THRESHOLD:
            return states[2]
        return states[3]

    elif currentState == states[4]: # treat trashing
        return states[4]
    return currentState

