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
        <div v-for="(recipe, index) in recipes" :key="index" class="shadow-md p-4 rounded-lg bg-white cursor-pointer" @click="goToRecipeDetail(recipe.id)">
          <img :src="recipe.image" alt="Recipe image" class="w-full h-48 object-cover" />
          <div class="mt-4">
            <h3 class="text-xl font-bold text-gray-900">{{ recipe.title }}</h3>
            <p class="mt-2 text-sm text-gray-600">By {{ recipe.created_by }}</p>
            <p class="mt-2 text-sm text-gray-600">{{ recipe.description }}</p>
            <div class="flex items-center mt-2">
              <span v-for="star in 5" :key="star" class="text-yellow-500">
                <StarIcon v-if="star <= recipe.rating" class="h-5 w-5" />
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
import { ref, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import { PlusIcon, StarIcon } from 'lucide-vue-next';
import { isAuthenticated } from '../services/userService.js';
import recipeService  from '../services/recipeService.js';

// const recipes = ref([
//   {
//     id: 1,
//     title: 'Spaghetti Carbonara',
//     description: 'Ein klassisches italienisches Gericht mit Speck, Eiern und Parmesan.',
//     created_by: 'Chef Luigi',
//     image: 'https://example.com/spaghetti-carbonara.jpg',
//     rating: 4
//   },
//   {
//     id: 2,
//     title: 'Caesar Salad',
//     description: 'Ein frischer Salat mit Römersalat, Croutons und Caesar-Dressing.',
//     created_by: 'Chef Julia',
//     image: 'https://example.com/caesar-salad.jpg',
//     rating: 5
//   },
//   {
//     id: 3,
//     title: 'Schokoladenkuchen',
//     description: 'Ein reichhaltiger und feuchter Schokoladenkuchen, perfekt für jeden Anlass.',
//     created_by: 'Chef Anna',
//     image: 'https://example.com/chocolate-cake.jpg',
//     rating: 3
//   }
// ]);

const recipes = ref([]);


const router = useRouter();

function showRecipeForm() {
  router.push('/create_recipe/');
}

function goToRecipeDetail(id) {
  router.push(`/recipe/${id}`);
}

onMounted(async () => {
  console.log('Home component is mounted');
  try {
    const recipeResponse = await recipeService.getRecipes();
    for (let recipe of recipeResponse.data) {
      const starResponse = await recipeService.getAverageStarsPerRecipe(recipe.id);
      recipe.rating = starResponse.data;
    }
    console.log('Fetched recipes:', recipeResponse.data);
    recipes.value = recipeResponse.data;
  } catch (error) {
    console.error("Error fetching applications:", error);
  }
});
</script>