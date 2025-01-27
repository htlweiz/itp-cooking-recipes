import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import LoginView from '../views/LoginView.vue'
import CreateRecipeView from '../components/Recipe.vue'
import { isAuthenticated } from '../services/user';

const routes = [
  { path: '/', redirect: '/home' },
  { path: '/home', component: HomeView },
  { path: '/login', component: LoginView },
  { path: '/create_recipe', component: CreateRecipeView },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

router.beforeEach((to, from, next) => {
  if (to.path === '/create_recipe' && !isAuthenticated()) {
    next('/login');
  } else {
    next();
  }
});

export default router;
