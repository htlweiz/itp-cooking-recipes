<template>
    <div class="min-h-screen flex items-center justify-center bg-gray-100 px-4 sm:px-6 lg:px-8">
      <div class="max-w-md w-full space-y-8 bg-white p-10 rounded-xl shadow-md">
        <div class="text-center">
          <h2 class="mt-6 text-3xl font-extrabold text-gray-900">Login</h2>
        </div>
        <form @submit.prevent="handleSubmit" class="mt-8 space-y-6">
          <div class="rounded-md shadow-sm -space-y-px">
            <div>
              <label for="email" class="sr-only">Email address</label>
              <div class="relative">
                <div class="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none z-10">
                  <MailIcon class="h-5 w-5 text-gray-400" />
                </div>
                <input 
                  id="email"
                  name="email"
                  type="email"
                  autocomplete="email"
                  required
                  v-model="email"
                  class="appearance-none rounded-none relative block w-full px-3 py-2 pl-10 border border-gray-300 placeholder-gray-500 
                  text-gray-900 rounded-t-md focus:outline-none focus:ring-indigo-500 focus:border-indigo-500  sm:text-sm"
                  placeholder="Email address"
                />
              </div>
            </div>
            <div>
              <label for="password" class="sr-only">Password</label>
              <div class="relative">
                <div class="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none z-10">
                  <LockIcon class="h-5 w-5 text-gray-400" />
                </div>
                <input
                  :type="showPassword ? 'text' : 'password'"
                  id="password"
                  name="password"
                  autocomplete="current-password"
                  required
                  v-model="password"
                  class="appearance-none rounded-none relative block w-full px-3 py-2 pl-10 pr-10 border border-gray-300 
                  placeholder-gray-500 text-gray-900 rounded-b-md focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm"
                  placeholder="Password"
                />
                <div class="absolute inset-y-0 right-0 pr-3 flex items-center z-10">
                  <button
                    type="button"
                    @click="togglePassword"
                    class="focus:outline-none"
                  >
                    <EyeIcon v-if="!showPassword" class="h-5 w-5 text-gray-400 hover:text-gray-500" />
                    <EyeOffIcon v-else class="h-5 w-5 text-gray-400 hover:text-gray-500" />
                  </button>
                </div>
              </div>
            </div>
          </div>
  
          <div>
            <button
              type="submit"
              :disabled="isLoading"
              class="group relative w-full flex justify-center py-2 px-4 border border-transparent text-sm font-medium 
              rounded-md text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 
              focus:ring-indigo-500 disabled:opacity-50 disabled:cursor-not-allowed"
            >
              {{ isLoading ? 'Logging in...' : 'Log In' }}
            </button>
          </div>
        </form>
        <p v-if="errorMessage" class="mt-2 text-center text-sm text-red-600">
          {{ errorMessage }}
        </p>
      </div>
    </div>
</template>

<script setup>
import { ref } from 'vue';
import { MailIcon, LockIcon, EyeIcon, EyeOffIcon } from 'lucide-vue-next';
import { useRouter } from 'vue-router';
import { login } from '../services/user';

const router = useRouter();

const email = ref('');
const password = ref('');
const showPassword = ref(false);
const isLoading = ref(false);
const errorMessage = ref('');
let isAuthenticated = ref(false);

function togglePassword() {
    showPassword.value = !showPassword.value;
}

function handleSubmit() {
    isLoading.value = true;
    errorMessage.value = '';
    
    setTimeout(() => {
        console.log('Email:', email.value);
        console.log('Password:', password.value);
        if (email.value === 'test@example.com' && password.value === 'password') {
            login('mock-token', email.value);
            router.push('/');
        } else {
            errorMessage.value = 'Invalid email or password';
        }
        isLoading.value = false;
    }, 1500);
}
</script>