import Vue from 'vue';
import vmodal from 'vue-js-modal';
import Notifications from 'vue-notification';
import VueHighcharts from 'vue-highcharts';
import VTooltip from 'v-tooltip';

import App from './App.vue';

Vue.config.productionTip = false;

Vue.use(vmodal);
Vue.use(VTooltip);
Vue.use(Notifications);
Vue.use(VueHighcharts);

new Vue({
  render: h => h(App)
}).$mount('#app');
