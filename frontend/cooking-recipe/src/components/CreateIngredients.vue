<template>
    <div class="min-h-screen bg-gray-100 flex items-center justify-center py-12 px-4 sm:px-6 lg:px-8">
      <div class="max-w-2xl w-full space-y-8 bg-white p-10 rounded-xl shadow-md">
        <div class="flex justify-between items-center">
          <router-link to="/ingredients" class="text-indigo-600 hover:text-indigo-800 focus:outline-indigo-500">
            <ArrowLeftIcon color="black" class="h-8 w-8" />
          </router-link>
          <div>
            <h2 class="text-center text-3xl font-extrabold text-gray-900">
              {{ editMode ? 'Zutat bearbeiten' : 'Neue Zutat hinzufügen' }}
            </h2>
          </div>
          <div class="w-8"></div>
        </div>
        <div class="mt-8">
          <form @submit.prevent="saveIngredient" class="space-y-4">
            <div>
              <label for="name" class="block text-sm font-medium text-gray-700">Name</label>
              <input 
                id="name" 
                type="text" 
                v-model="currentIngredient.name" 
                required
                class="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-indigo-500"
                placeholder="Name der Zutat"
              />
            </div>
            <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div>
                <label for="calories" class="block text-sm font-medium text-gray-700">Kalorien (kcal)</label>
                <input 
                  id="calories" 
                  type="number" 
                  v-model="currentIngredient.calories"  
                  required
                  min="0" 
                  step="1"
                  class="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-indigo-500"
                  placeholder="Kalorien pro 100g/ml"
                />
              </div>
              <div>
                <label for="protein" class="block text-sm font-medium text-gray-700">Protein (g)</label>
                <input 
                  id="protein" 
                  type="number" 
                  v-model="currentIngredient.protein" 
                  min="0" 
                  step="0.1"
                  class="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-indigo-500"
                  placeholder="Protein pro 100g/ml"
                />
              </div>
              <div>
                <label for="carbs" class="block text-sm font-medium text-gray-700">Kohlenhydrate (g)</label>
                <input 
                  id="carbs" 
                  type="number" 
                  v-model="currentIngredient.carbs"  
                  required
                  min="0" 
                  step="0.1"
                  class="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-indigo-500"
                  placeholder="Kohlenhydrate pro 100g/ml"
                />
              </div>
              <div>
                <label for="fat" class="block text-sm font-medium text-gray-700">Fett (g)</label>
                <input 
                  id="fat" 
                  type="number" 
                  v-model="currentIngredient.fat"  
                  required
                  min="0" 
                  step="0.1"
                  class="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-indigo-500"
                  placeholder="Fett pro 100g/ml"
                />
              </div>
            </div>
            <div class="flex justify-end space-x-3">
              <button 
                type="button" 
                @click="resetForm"
                class="px-4 py-2 border border-gray-300 rounded-md shadow-sm text-sm font-medium text-gray-700 bg-white hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500"
              >
                Abbrechen
              </button>
              <button 
                type="submit"
                class="px-4 py-2 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500"
              >
                {{ editMode ? 'Aktualisieren' : 'Hinzufügen' }}
              </button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import { ArrowLeftIcon } from 'lucide-vue-next';
import recipeService from '../services/recipeService.js';

const router = useRouter();

const currentIngredient = ref({
  name: '',
  calories: 0,
  protein: 0,
  carbs: 0,
  fat: 0
});
const editMode = ref(false);

const query = new URLSearchParams(window.location.search);
const ingredientId = query.get('id');

async function fetchIngredient() {
  try {
    const response = await recipeService.getIngredient(ingredientId);
    currentIngredient.value = response.data || [];
  } catch (error) {
    console.error('Fehler beim Laden der Zutaten:', error);
  }
}

onMounted(async () => {
  if (ingredientId) {
  editMode.value = true;
  await fetchIngredient(ingredientId);
}

});
async function saveIngredient() {
  if (editMode.value) {
    try {
      await recipeService.updateIngredient(ingredientId, currentIngredient.value);
      router.push('/ingredients'); 
    } catch (error) {
      console.error('Fehler beim Aktualisieren der Zutat:', error);
    }
  } else {
    try {
      const response = await recipeService.createIngredient(currentIngredient.value);
      router.push('/ingredients'); 
    } catch (error) {
      console.error('Fehler beim Erstellen der Zutat:', error);
    }
  }
  
  resetForm();
}

function resetForm() {
  currentIngredient.value = {
    name: '',
    calories: 0,
    protein: 0,
    carbs: 0,
    fat: 0
  };
  editMode.value = false;
}
</script>
  
  