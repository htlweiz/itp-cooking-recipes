import { createRouter, createWebHistory } from 'vue-router';
import HomeView from '../views/HomeView.vue';
import LoginView from '../views/LoginView.vue';
import RecipeDetailView from '../views/RecipeDetailView.vue';
import CreateRecipeView from '../views/CreateRecipeView.vue';
import UpdateRecipeView from '../views/UpdateRecipeView.vue';
import { isAuthenticated } from '../services/userService';
import CreateIngredientView  from '../views/CreateIngredientView.vue';
import IngredientView  from '../views/IngredientView.vue';

const routes = [
  { path: '/', name: 'Home', component: HomeView },
  { path: '/login', name: 'Login', component: LoginView },
  { path: '/recipe/:id', name: 'RecipeDetail', component: RecipeDetailView, props: true },
  { path: '/create_recipe', name: 'CreateRecipe', component: CreateRecipeView },
  { path: '/update_recipe/:id', name: 'UpdateRecipe', component: UpdateRecipeView, props: true },
  { path: '/ingredients', name: 'Ingredient', component: IngredientView },
  { path: '/create_ingredients', name: 'CreateIngredient', component: CreateIngredientView },
];  

const router = createRouter({
  history: createWebHistory(),
  routes
});

router.beforeEach((to, from, next) => {
  if (to.path === '/create_recipe/' && !isAuthenticated()) {
    next('/login');
  }
  if (to.path.startsWith('/update_recipe/') && !isAuthenticated()) {
    next('/login');
  }
  next();
});

export default router;
