<template>
  <div class="min-h-screen bg-gray-100 py-6 px-4 sm:px-6 lg:px-8">
    <div class="max-w-3xl mx-auto">
      <router-link to="/" class="inline-flex items-center text-indigo-600 hover:text-indigo-800 focus:outline-indigo-500 mb-6 absolute top-4 left-4">
          <ArrowLeftIcon class="h-6 w-6 mr-2" />
          Zurück zur Startseite
      </router-link>
        
        <div class="bg-white shadow overflow-hidden sm:rounded-lg mt-6">
            <div class="px-4 py-5 sm:p-6">
                <div v-if="recipe.image">
                  <img :src="recipe.image" :alt="recipe.title" class="w-full h-64 object-cover rounded-lg shadow-md mb-6">
                </div>
                <div v-else class="flex flex-col items-center justify-center h-64 border-2 border-dashed border-gray-300 rounded-lg">
                  <p class="text-gray-500 mb-4">Kein Bild vorhanden</p>
                  <input type="file" @change="uploadImage" accept="image/*" class="hidden" ref="fileInput">
                  <button
                    @click="triggerFileInput"
                    class="bg-indigo-600 hover:bg-indigo-700 text-white font-semibold py-2 px-4 rounded-md"
                  >
                    Bild hochladen
                  </button>
                </div>
                <h2 class="text-3xl font-extrabold text-gray-900 mb-2 break-words">{{ recipe.title }}</h2>
                <p class="text-gray-600 mb-4 break-words">{{ recipe.description }}</p>
                <div class="flex items-center mb-4">
                  <button
                    v-for="star in 5"
                    :key="star"
                    @click="giveStar(star)"
                    class="focus:outline-none"
                  >
                    <StarIcon
                      :class="{
                        'text-yellow-400': star <= Math.floor(recipe.average_stars),
                        'text-gray-300': star > Math.floor(recipe.average_stars),
                      }"
                      class="h-5 w-5"
                    />
                  </button>
                  <span class="ml-2 text-gray-600">({{ recipe.average_stars }})</span>
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
import userService from '../services/userService.js';

const route = useRoute();
const router = useRouter();
const recipeId = route.params.id;

const recipe = ref({
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
});

const isCreator = ref(false);

const fileInput = ref(null);

onMounted(async () => {
  isCreator.value = true;
  try {
    const recipeResponse = await recipeService.getRecipe(recipeId);
    recipe.value = recipeResponse.data;
    
    const userResponse = await (userService.getUser(recipe.value.related_user_id))
    recipe.value.created_by = userResponse.data.username;
    console.log(recipe.value);

    const imageResponse = await recipeService.getRecipePic(recipeResponse.data.id);
    if (imageResponse.data.type === 'image/jpeg' || imageResponse.data.type === 'image/png' ) {
      const blob = new Blob([imageResponse.data], { type: 'image/png' })
      recipe.value.image = URL.createObjectURL(blob);
    } 
  } catch (error) {
    console.error("Error fetching applications:", error);
  }
});


function triggerFileInput() {
  fileInput.value.click();
}

async function uploadImage(event) {
  const file = event.target.files[0];
  if (!file) return;

  try {
    const formData = new FormData();
    formData.append('file', file); 

    await recipeService.uploadRecipePic(recipeId, formData);

    const imageResponse = await recipeService.getRecipePic(recipeId);
    const blob = new Blob([imageResponse.data], { type: file.type });
    recipe.value.image = URL.createObjectURL(blob)

  } catch (error) {
    console.error('Fehler beim Hochladen des Bildes:', error);
  }
}

async function giveStar(star) {
  try {
    const starResponse = await recipeService.getStars();
    const starToUpdate = starResponse.data.find(
      (s) => s.related_recipe_id === recipe.value.id && s.related_user_id === recipe.value.related_user_id
    );

    if (starToUpdate) {
      await recipeService.updateStar(starToUpdate.id, {
        rating: star,
      });
    } else {
      await recipeService.createStar({
        rating: star,
        related_recipe_id: recipe.value.id,
      });
    }

    const updatedRecipe = await recipeService.getRecipe(recipeId);
    recipe.value.average_stars = updatedRecipe.data.average_stars;

  } catch (error) {
    console.error('Fehler beim Aktualisieren der Bewertung:', error);
  }
}

function getNutritionalInfo() {
  const totalCalories = recipe.value.ingredients.reduce((sum, ing) => sum + (ing.calories * ing.amount ), 0);
  const totalProtein = recipe.value.ingredients.reduce((sum, ing) => sum + (ing.protein * ing.amount ), 0) + 'g';
  const totalCarbs = recipe.value.ingredients.reduce((sum, ing) => sum + (ing.carbs * ing.amount ), 0) + 'g';
  const totalFat = recipe.value.ingredients.reduce((sum, ing) => sum + (ing.fat * ing.amount ), 0) + 'g';

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

<style scoped>
.break-words {
  word-wrap: break-word;
  word-break: break-word; 
  white-space: normal;
}
</style>