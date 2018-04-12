import Vue from 'vue';
import VTooltip from 'v-tooltip';
import VueModal from 'vue-js-modal';
import VueCookies from 'vue-cookies';
import Notifications from 'vue-notification';
import VueHighcharts from 'vue-highcharts';

import App from './App.vue';

Vue.config.productionTip = false;

Vue.use(VTooltip);
Vue.use(VueModal);
Vue.use(VueCookies);
Vue.use(Notifications);
Vue.use(VueHighcharts);

new Vue({
  render: h => h(App)
}).$mount('#app');
