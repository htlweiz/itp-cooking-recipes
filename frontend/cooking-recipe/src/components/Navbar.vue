<template>
  <nav class="bg-white shadow-md">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
      <div class="flex justify-between h-16">
        <div class="flex items-center">
          <a href="/" class="inline-flex items-center">
            <UtensilsCrossedIcon class="h-8 w-8 text-indigo-600" />
            <span class="ml-2 text-xl font-bold text-gray-800">RecipeSense</span>
          </a>
        </div>
        <div class="flex items-center">
          <div class="hidden sm:block">
            <div class="relative">
              <input
                type="text"
                placeholder="Rezept suchen..."
                class="w-full sm:w-64 px-4 py-2 text-sm text-gray-700 bg-gray-100 rounded-full focus:outline-none focus:ring-2 focus:ring-indigo-500"
                v-model="searchQuery"
                @keyup.enter="performSearch"
              />
              <button
                @click="performSearch"
                class="absolute right-0 top-0 mt-2 mr-4 text-gray-400 hover:text-gray-600"
              >
                <SearchIcon class="h-5 w-5" />
              </button>
            </div>
          </div>
          <div class="ml-6 flex items-center hidden sm:block">
            <a
              href="/login"
              class="inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md text-white bg-indigo-600 
              hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500"
            >
              <UserIcon class="h-5 w-5 mr-2" />
              Login
            </a>
          </div>
          <button
            class="sm:hidden text-gray-500 hover:text-gray-700 focus:outline-none"
            @click="toggleSearchBar"
          >
            <SearchIcon class="h-6 w-6" />
          </button>
          <button
            class="inline-flex items-center justify-center p-2 rounded-md text-gray-400 hover:text-gray-500 hover:bg-gray-100 focus:outline-none focus:ring-2 focus:ring-inset focus:ring-indigo-500 sm:hidden ml-2"
            @click="toggleMobileMenu"
          >
            <MenuIcon v-if="!isMobileMenuOpen" class="h-6 w-6" />
            <XIcon v-else class="h-6 w-6" />
          </button>
        </div>
      </div>
    </div>
    <div v-if="isSearchBarOpen" class="bg-gray-100 px-4 py-2 sm:hidden">
      <div class="flex items-center">
        <input
          type="text"
          placeholder="Rezept suchen..."
          class="w-full px-4 py-2 text-sm text-gray-700 bg-white rounded-full focus:outline-none focus:ring-2 focus:ring-indigo-500"
          v-model="searchQuery"
          @keyup.enter="performSearch"
        />
        <button @click="performSearch" class="ml-2 text-gray-500 hover:text-gray-700">
          <SearchIcon class="h-5 w-5" />
        </button>
      </div>
    </div>
    <div v-if="isMobileMenuOpen" class="sm:hidden">
      <div class="pt-2 pb-3 space-y-1">
        <a href="#" class="block px-3 py-2 rounded-md text-base font-medium text-gray-700 hover:text-gray-900 hover:bg-gray-50">Rezepte</a>
        <a
          href="/login"
          class="block px-3 py-2 rounded-md text-base font-medium text-gray-700 hover:text-gray-900 hover:bg-gray-50"
        >
          Login
        </a>
      </div>
    </div>
  </nav>
</template>
  
<script setup>
import { ref } from 'vue';
import { UtensilsCrossedIcon, SearchIcon, UserIcon, MenuIcon, XIcon } from 'lucide-vue-next';

const searchQuery = ref('');
const isMobileMenuOpen = ref(false);
const isSearchBarOpen = ref(false);
  
function performSearch() {
  console.log('Suche nach:', searchQuery.value);
}

function toggleMobileMenu() {
  isMobileMenuOpen.value = !isMobileMenuOpen.value;
}

function toggleSearchBar() {
  isSearchBarOpen.value = !isSearchBarOpen.value;
}
</script>
  