<template>
    <div class="min-h-screen bg-gray-100">
        <Navbar />
        <div class="max-w-7xl mx-auto py-6 sm:px-6 lg:px-8">
            <div class="bg-white shadow overflow-hidden sm:rounded-lg p-6">
                <div class="flex justify-between items-center mb-6">
                    <h2 class="text-2xl font-bold text-gray-900">Zutatenübersicht</h2>
                    <router-link to="/create_ingredients" class="bg-indigo-600 hover:bg-indigo-700 text-white font-semibold py-2 px-4 rounded-md">
                        Neue Zutat hinzufügen
                    </router-link>
                </div>
                <div class="overflow-x-auto">
                    <table class="min-w-full divide-y divide-gray-200">
                        <thead class="bg-gray-50">
                            <tr>
                                <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Name</th>
                                <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Kalorien</th>
                                <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Protein</th>
                                <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Kohlenhydrate</th>
                                <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Fett</th>
                                <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Aktionen</th>
                            </tr>
                        </thead>
                        <tbody class="bg-white divide-y divide-gray-200">
                            <tr v-for="(ingredient, index) in ingredients" :key="index" class="hover:bg-gray-50">
                                <td class="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">{{ ingredient.name }}</td>
                                <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">{{ ingredient.calories }} kcal</td>
                                <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">{{ ingredient.protein }} g</td>
                                <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">{{ ingredient.carbs }} g</td>
                                <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">{{ ingredient.fat }} g</td>
                                <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500 flex space-x-2">
                                    <router-link :to="`/create_ingredients?id=${ingredient.id}`" class="text-indigo-600 hover:text-indigo-900 ">
                                        <PencilIcon class="h-5 w-5" />
                                    </router-link>
                                    <button @click="deleteIngredient(ingredient.id)" class="text-red-600 hover:text-red-900">
                                        <TrashIcon class="h-5 w-5" />
                                    </button>
                                </td>
                            </tr>
                        </tbody>
                    </table>
                </div>
            </div>
        </div>
    </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import Navbar from '../components/Navbar.vue';
import { PencilIcon, TrashIcon } from 'lucide-vue-next';
import recipeService from '../services/recipeService.js';

const ingredients = ref([]);

async function fetchIngredients() {
    try {
        const queryParams = {
            page: 0,
            page_size: 1000,
        };
        const response = await recipeService.getIngredients(queryParams);
        ingredients.value = response.data || [];
    } catch (error) {
        console.error('Fehler beim Laden der Zutaten:', error);
    }
}

onMounted(async () => {
    await fetchIngredients();
});

async function deleteIngredient(ingredientId) {
    if (confirm('Sind Sie sicher, dass Sie diese Zutat löschen möchten?')) {
        await recipeService.deleteIngredient(ingredientId);
        await fetchIngredients();
    }
}
</script>