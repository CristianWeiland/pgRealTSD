import Vue from 'vue';
import Vuex from 'vuex';

Vue.use(Vuex);

export default new Vuex.Store({
    state: {
        configurations: {},
        loading: {
            show: false,
        },
        intervals: [],
    },
    mutations: {
        setConfigs(state, configurations) {
            state.configurations = configurations;
        },
        setLoading(state, val) {
            state.loading.show = val;
        },
        createInterval(state, interval) {
            state.intervals.push(interval);
        },
        removeIntervals(state) {
            state.intervals.forEach((id) => {
                clearInterval(id);
            });
        },
    },
});
