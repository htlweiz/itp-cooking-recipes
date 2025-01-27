<template>
    <div class="min-h-screen bg-gray-100">
      <Navbar />
      <main class="max-w-7xl mx-auto py-6 sm:px-6 lg:px-8">
        <div class="px-4 py-6 sm:px-0">
          <h1 class="text-3xl font-bold text-gray-900">Willkommen bei RecipeSense</h1>
          <p class="mt-4 text-lg text-gray-600">Entdecken Sie köstliche Rezepte und teilen Sie Ihre kulinarischen Kreationen mit der Welt.</p>
        </div>
        <div class="floating-action-button">
          <button
            class="fixed bottom-10 right-12 bg-indigo-600 hover:bg-indigo-700 text-white font-semibold p-4 
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
import RecipeForm from './Recipe.vue';
import { ref } from 'vue';
import {useRouter} from 'vue-router';
import { PlusIcon } from 'lucide-vue-next';

const router = useRouter();

function showRecipeForm() {
  router.push('/create_recipe/');
}
</script>