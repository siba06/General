import { createRouter, createWebHistory } from 'vue-router'
import { auth } from '../firebase/init.js';

const routes = [
  {
    path: '/pending',
    name: 'PendingApproval',
    meta:{
      requiresAuth : true,
    },
    // route level code-splitting
    // this generates a separate chunk (about.[hash].js) for this route
    // which is lazy-loaded when the route is visited.
    component: () => import(/* webpackChunkName: "pending" */'../views/PendingApprovalView.vue')
  },
  {
  path: '/',
  name: 'Login',

  // route level code-splitting
  // this generates a separate chunk (about.[hash].js) for this route
  // which is lazy-loaded when the route is visited.
  component: () => import(/* webpackChunkName: "login" */'../views/LoginView.vue')

  },
  {
    path: '/completed',
    name: 'Completed',
    meta:{
      requiresAuth : true,
    },
    component: () => import(/* webpackChunkName: "about" */'../views/CompletedView.vue')
  },
  {
    path: '/about',
    name: 'about',
    meta:{
      requiresAuth : true,
    },
    component: () => import(/* webpackChunkName: "about" */ '../views/AboutView.vue')
  },
  {
    path: '/settings',
    name: 'settings',
    meta:{
      requiresAuth : true,
    },
    component: () => import(/* webpackChunkName: "about" */ '../views/SettingsView.vue')
  },
  {
    path: '/volume/:id/:vol/:patient',
    name:'volume',
    meta:{
      requiresAuth : true,
    },
    component: () => import(/* webpackChunkName: "about" */ '../views/VolumeView.vue')
  }
]

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes
});

router.beforeEach((to,from,next) => {
  const authenticatedUser = auth.currentUser;
  const requiresAuth = to.matched.some(record => record.meta.requiresAuth);
  if (requiresAuth && !authenticatedUser) next('')
  else next()
});



export default router
