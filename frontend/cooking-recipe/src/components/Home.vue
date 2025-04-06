<template>
  <div class="min-h-screen bg-gray-100">
    <Navbar />
    <main class="max-w-7xl mx-auto py-6 sm:px-6 lg:px-8">
      <div class="px-4 py-6 sm:px-0">
        <h1 class="text-3xl font-bold text-gray-900">Willkommen bei RecipeSense</h1>
        <p class="mt-4 text-lg text-gray-600">Entdecken Sie köstliche Rezepte und teilen Sie Ihre kulinarischen Kreationen mit der Welt.</p>
      </div>
      <div class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-4">
        <div v-if="recipes.length === 0" class="text-center text-gray-600 mt-8">
          <p class="text-lg">Keine Rezepte gefunden.</p>
        </div>
        <div v-for="(recipe, index) in filteredRecipes" :key="index" class="shadow-md p-4 rounded-lg bg-white cursor-pointer" @click="goToRecipeDetail(recipe.id)">
          <img :src="recipe.image" alt="Recipe image" class="w-full h-48 object-cover" />
          <div class="mt-4">
            <h3 class="text-xl font-bold text-gray-900 truncate">{{ recipe.title }}</h3>
            <p class="mt-2 text-sm text-gray-600">By {{ recipe.created_by }}</p>
            <p class="mt-2 text-sm text-gray-600 truncate">{{ recipe.description }}</p>
            <div class="flex items-center mt-2">
              <span v-for="star in 5" :key="star" class="text-yellow-500">
                <StarIcon v-if="star <= recipe.average_stars" class="h-5 w-5" />
                <StarIcon v-else class="h-5 w-5 text-gray-300" />
              </span>
            </div>
          </div>
        </div>
      </div>
      <div v-if="isAuthenticated()" class="floating-action-button">
        <button
          class="fixed bottom-10 right-8 sm:right-12 bg-indigo-600 hover:bg-indigo-700 text-white font-semibold p-4 
          rounded-full shadow-md transition-all duration-300 ease-in-out transform hover:scale-110 focus:outline-none"
          @click="showRecipeForm"
        >
          <PlusIcon class="h-6 w-6" />
        </button>
      </div>
    </main>
  </div>
</template>

<script setup>
import Navbar from './Navbar.vue';
import { ref, onMounted, computed } from 'vue';
import { useRouter } from 'vue-router';
import { PlusIcon, StarIcon } from 'lucide-vue-next';
import { isAuthenticated } from '../services/userService.js';
import userService from '../services/userService.js';
import recipeService  from '../services/recipeService.js';
import { searchQuery } from '../services/searchState';

const recipes = ref([{
  id: null,
  title: '',
  description: '',
  ingredients: [
    { id: null, name: '', amount: null, unit: '', calories: null, protein: null, carbs: null, fat: null }
  ],
  steps: [
    { instruction: '' }
  ],
  average_stars: null,
  related_user_id: null,
  created_by: null,
  image: null
}]);

const router = useRouter();

const filteredRecipes = computed(() => {
  if (!searchQuery.value) {
    return recipes.value;
  }
  return recipes.value.filter(recipe =>
    recipe.title.toLowerCase().includes(searchQuery.value.toLowerCase()) ||
    recipe.description.toLowerCase().includes(searchQuery.value.toLowerCase())
  );
});

function showRecipeForm() {
  router.push('/create_recipe/');
}

function goToRecipeDetail(id) {
  router.push(`/recipe/${id}`);
}

onMounted(async () => {
  try {
    const recipeResponse = await recipeService.getRecipes();
    for (let i = 0; i < recipeResponse.data.length; i++) {
      const userResponse = await userService.getUser(recipeResponse.data[i].related_user_id);
      recipeResponse.data[i].created_by = userResponse.data.username;
    }

    for (let i = 0; i < recipeResponse.data.length; i++) {
      const imageResponse = await recipeService.getRecipePic(recipeResponse.data[i].id);
      const blob = new Blob([imageResponse.data], { type: 'image/png' })
      recipeResponse.data[i].image = URL.createObjectURL(blob);
    } 
    recipes.value = recipeResponse.data;
  } catch (error) {
    console.error("Error fetching applications:", error);
  }
});
</script>

<style scoped>
.truncate {
  overflow: hidden;
  white-space: nowrap;
  text-overflow: ellipsis;
}
</style>