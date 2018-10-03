import Vue from 'vue';
import Vuex from 'vuex';

Vue.use(Vuex);

export default new Vuex.Store({
    state: {
        configurations: {},
        loading: {
            show: false,
        },
        selectedServerIndex: -1,
        server: null,
        servers: [],
        intervals: [],
    },
    mutations: {
        setConfigs(state, configurations) {
            state.configurations = configurations;
        },
        setLoading(state, val) {
            state.loading.show = val;
        },
        setServers(state, val) {
            state.servers = val;
        },
        selectServer(state, data) {
            state.server = data.server;
            state.selectedServerIndex = data.idx;
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
    getters: {
        servers(state) {
            return state.servers;
        },
        selectedServerIndex(state) {
            return state.selectedServerIndex;
        },
        selectedServer(state) {
            return state.server;
        },
        configurations(state) {
            return state.configurations;
        },
    },
});
