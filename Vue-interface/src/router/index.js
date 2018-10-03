import VueRouter from 'vue-router';

import Configurations from '@/components/Configurations';
import MainContent from '@/components/MainContent';

const routes = [
  {
    path: '/',
    name: 'main',
    component: MainContent,
  },
  {
    path: '/configs',
    name: 'configs',
    component: Configurations,
  },
];

const router = new VueRouter({
  routes,
});

export default router;
