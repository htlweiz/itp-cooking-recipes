<template>
  <div class="min-h-screen bg-gray-100 py-6 px-4 sm:px-6 lg:px-8">
      <div class="max-w-3xl mx-auto">
          <router-link to="/" class="inline-flex items-center text-indigo-600 hover:text-indigo-800 focus:outline-indigo-500 mb-6 absolute top-4 left-4">
              <ArrowLeftIcon class="h-6 w-6 mr-2" />
              Zurück zur Startseite
          </router-link>
          
          <div class="bg-white shadow overflow-hidden sm:rounded-lg mt-6">
              <div class="px-4 py-5 sm:p-6">
                  <img :src="recipe.image" :alt="recipe.title" class="w-full h-64 object-cover rounded-lg shadow-md mb-6">
                  <h2 class="text-3xl font-extrabold text-gray-900 mb-2">{{ recipe.title }}</h2>
                  <p class="text-gray-600 mb-4">{{ recipe.description }}</p>
                  <div class="flex items-center mb-4">
                      <StarIcon v-for="i in Math.floor(recipe.rating)" :key="i" class="h-5 w-5 text-yellow-400" />
                      <StarIcon v-for="i in 5 - Math.floor(recipe.rating)" :key="i + 5" class="h-5 w-5 text-gray-300" />
                      <span class="ml-2 text-gray-600">({{ recipe.rating }})</span>
                  </div>
                  <p class="text-sm text-gray-500 mb-6">Erstellt bei {{ recipe.created_by }}</p>

                  <div class="mb-8">
                      <h3 class="text-xl font-semibold text-gray-900 mb-4">Zutaten</h3>
                      <ul class="space-y-2">
                      <li v-for="(ingredient, index) in recipe.ingredients" :key="index" class="flex justify-between items-center">
                          <span>{{ ingredient.name }}</span>
                          <span class="text-gray-600">{{ ingredient.amount }} {{ ingredient.unit }}</span>
                      </li>
                      </ul>
                  </div>

                  <div class="mb-8">
                      <h3 class="text-xl font-semibold text-gray-900 mb-4">Schritte</h3>
                      <ol class="list-decimal list-inside space-y-2">
                      <li v-for="(step, index) in recipe.steps" :key="index" class="text-gray-700">
                          {{ step.instruction }}
                      </li>
                      </ol>
                  </div>

                  <div>
                      <h3 class="text-xl font-semibold text-gray-900 mb-4">Nährwerte</h3>
                      <div class="bg-gray-100 rounded-lg p-4 grid grid-cols-2 gap-4">
                          <div v-for="(nutrient, name) in getNutritionalInfo()" :key="name" class="text-center">
                              <p class="text-lg font-semibold text-gray-700">{{ nutrient }}</p>
                              <p class="text-sm text-gray-500">{{ name }}</p>
                          </div>
                      </div>
                  </div>

                  <div v-if="isCreator" class="mt-6 flex justify-end space-x-4">
                      <button @click="updateRecipe" class="bg-indigo-600 hover:bg-indigo-700 text-white font-semibold py-2 px-4 rounded-md">
                          Rezept bearbeiten
                      </button>
                      <button @click="deleteRecipe" class="bg-red-600 hover:bg-red-700 text-white font-semibold py-2 px-4 rounded-md">
                          Rezept Löschen
                      </button>
                  </div>
              </div>
          </div>
      </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import { ArrowLeftIcon, StarIcon } from 'lucide-vue-next';
import recipeService  from '../services/recipeService.js';

const route = useRoute();
const router = useRouter();
const recipeId = route.params.id;

const recipe = ref({
id: 1,
title: 'Spaghetti Carbonara',
description: 'Ein klassisches italienisches Gericht mit Speck, Eiern und Parmesan.',
ingredients: [
  { name: 'Spaghetti', amount: 200, unit: 'g', calories: 300, protein: 10, carbs: 60, fat: 2 },
  { name: 'Speck', amount: 100, unit: 'g', calories: 500, protein: 20, carbs: 0, fat: 45 },
  { name: 'Eier', amount: 2, unit: 'Stück', calories: 150, protein: 12, carbs: 1, fat: 10 },
  { name: 'Parmesan', amount: 50, unit: 'g', calories: 200, protein: 18, carbs: 2, fat: 14 }
],
steps: [
  { instruction: 'Spaghetti in Salzwasser kochen.' },
  { instruction: 'Speck in einer Pfanne anbraten.' },
  { instruction: 'Eier und Parmesan vermischen.' },
  { instruction: 'Spaghetti abgießen und mit Speck und Eiermischung vermengen.' }
],
created_by: 'Chef Luigi',
image: 'https://example.com/spaghetti-carbonara.jpg',
rating: 4.5
});

const isCreator = ref(false);

onMounted(async () => {
console.log('Recipe ID:', recipeId);
isCreator.value = true;
try {
  const recipeResponse = await recipeService.getRecipe(recipeId);
  const starResponse = await recipeService.getAverageStarsPerRecipe(recipeResponse.data.id);
  recipeResponse.data.rating = starResponse.data;
  
  console.log('Fetched recipes:', recipeResponse.data);
  recipe.value = recipeResponse.data;
} catch (error) {
  console.error("Error fetching applications:", error);
}
});

function getNutritionalInfo() {
const totalCalories = recipe.value.ingredients.reduce((sum, ing) => sum + (ing.calories * ing.amount / 100), 0);
const totalProtein = recipe.value.ingredients.reduce((sum, ing) => sum + (ing.protein * ing.amount / 100), 0) + 'g';
const totalCarbs = recipe.value.ingredients.reduce((sum, ing) => sum + (ing.carbs * ing.amount / 100), 0) + 'g';
const totalFat = recipe.value.ingredients.reduce((sum, ing) => sum + (ing.fat * ing.amount / 100), 0) + 'g';

return {
  Kalorien: totalCalories,
  Protein: totalProtein,
  Kohlenhydrate: totalCarbs,
  Fett: totalFat
};
}

function updateRecipe() {
router.push(`/update_recipe/${recipe.value.id}`);
}

function deleteRecipe() {
if (!confirm('Möchtest du das Rezept wirklich löschen?')) {
  return;
}
try {
  recipeService.deleteRecipe(recipeId);
} catch (error) {
  console.error("Error deleting recipe:", error);
}
console.log('Rezept gelöscht');
router.push('/');
}

</script>