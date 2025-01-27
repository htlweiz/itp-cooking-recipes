<template>
    <div class="min-h-screen bg-gray-100 flex items-center justify-center py-12 px-4 sm:px-6 lg:px-8">
        <div class="max-w-2xl w-full space-y-8 bg-white p-10 rounded-xl shadow-md">
        <div>
            <h2 class="text-center text-3xl font-extrabold text-gray-900">Rezept erstellen</h2>
            <p class="mt-2 text-center text-sm text-gray-600">
            Fügen Sie alle Details Ihres Rezepts hinzu
            </p>
        </div>
        <form @submit.prevent="createRecipe" class="mt-8 space-y-6">
            <div class="space-y-4">
            <div>
                <label for="title" class="block text-sm font-medium text-gray-700">Titel</label>
                <input
                id="title"
                type="text"
                required
                v-model="recipe.title"
                class="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:ring-indigo-500 focus:border-indigo-500"
                placeholder="Titel des Rezepts"
                />
            </div>
            <div>
                <label for="description" class="block text-sm font-medium text-gray-700">Beschreibung</label>
                <textarea
                id="description"
                required
                v-model="recipe.description"
                rows="3"
                class="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:ring-indigo-500 focus:border-indigo-500"
                placeholder="Kurze Beschreibung des Rezepts..."
                ></textarea>
            </div>
            </div>
            <div>
                <label class="block text-sm font-medium text-gray-700">Zutaten</label>
                <div class="flex flex-wrap gap-2">
                    <label for="ingredients"> Name</label>
                    <input type="text" name="ingredients" id="ingredients" v-model="recipe.ingredients.name" class="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:ring-indigo-500 focus:border-indigo-500">
                    <label for="amount"> Menge</label>
                    <input type="text" name="amount" id="amount" v-model="recipe.ingredients.amount" class="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:ring-indigo-500 focus:border-indigo-500">
                    <label for="unit"> Einheit</label>
                    <input type="text" name="unit" id="unit" v-model="recipe.ingredients.unit" class="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:ring-indigo-500 focus:border-indigo-500">
                </div>
                <button>
                    <PlusIcon class="h-6 w-6" />
                </button>
                <div v-for="(ingredient, index) in recipe.ingredients" :key="index" class="flex items-center gap-2">
                    <span>{{ ingredient.name }} - {{ ingredient.amount }} {{ ingredient.unit }}</span>
                    <button @click="removeIngredient(index)">
                        <TrashIcon class="h-4 w-4" />
                    </button>
                </div>
            </div>
            
            <div>
            <button
                type="submit"
                class="w-full flex justify-center py-2 px-4 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500"
            >
                Rezept speichern
            </button>
            </div>
        </form>
        </div>
    </div>
</template>
  
<script setup>
import { ref } from 'vue'
import { PlusIcon, TrashIcon, ArrowUpIcon, ArrowDownIcon } from 'lucide-vue-next'

const recipe = ref({
    title: '',
    description: '',
    ingredients: [{ name: '', amount: '', unit: 'g' }],
    steps: [{ instruction: '' }]
})

function removeIngredient(index) {
    recipe.value.ingredients.splice(index, 1)
}

function createRecipe() {
    console.log('Neues Rezept:', recipe.value)
}

</script>
  
  