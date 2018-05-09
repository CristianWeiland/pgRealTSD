import Vue from 'vue';
import VTooltip from 'v-tooltip';
import VueModal from 'vue-js-modal';
import VueCookies from 'vue-cookies';
import Notifications from 'vue-notification';
import VueHighcharts from 'vue-highcharts';

import App from './App.vue';

import store from './store';

Vue.config.productionTip = false;

Vue.use(VTooltip);
Vue.use(VueModal);
Vue.use(VueCookies);
Vue.use(Notifications);
Vue.use(VueHighcharts);

new Vue({
    el: '#app',
    store,
    render: h => h(App)
});
