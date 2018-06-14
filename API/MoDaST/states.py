states = ['warmup', 'steady', 'under_pressure', 'stress', 'thrashing']
initialState = 'warmup'

WARMUP_THRESHOLD = 0.1
STEADY_THRESHOLD = 0.9
STRESS_THRESHOLD = 0.1
THRASHING_THRESHOLD = 1.0

def getNextState(currentState, performanceVariation, transactionTroughput, performanceTrend, transactionsTreated):
    if currentState == 0: # treat warmup
        if performanceVariation < WARMUP_THRESHOLD:
            return 1
        return 0

    elif currentState == 1: # treat steady
        if transactionTroughput > STEADY_THRESHOLD:
            return 1
        return 2

    elif currentState == 2: # treat under_pressure
        if performanceVariation > (STRESS_THRESHOLD * transactionsTreated):
            return 3
        if transactionTroughput > STEADY_THRESHOLD:
            return 1
        return 2

    elif currentState == 3: # treat stress
        if performanceTrend is not None and performanceTrend < (THRASHING_THRESHOLD * transactionTroughput):
            return 4
        if performanceVariation <= STRESS_THRESHOLD:
            return 2
        return 3

    elif currentState == 4: # treat trashing
        return 4
    return currentState

