import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import LoginView from '../views/LoginView.vue'
import CreateRecipeView from '../components/Recipe.vue'

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

export default router
