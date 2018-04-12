import Vue from 'vue';
import Vuex from 'vuex';

Vue.use(Vuex);

export default new Vuex.Store({
    state: {
        configurations: {},
        loading: {
            show: false,
        },
    },
    mutations: {
        setConfigs (state, configurations) {
            state.configurations = configurations;
        },
        setLoading (state, val) {
            state.loading.show = val;
        },
    },
});
