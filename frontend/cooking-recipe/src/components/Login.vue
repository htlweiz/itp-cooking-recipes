<template>
  <div class="min-h-screen flex items-center justify-center bg-gray-100 px-4 sm:px-6 lg:px-8">
    <div class="max-w-md w-full space-y-8 bg-white p-10 rounded-xl shadow-md">
      <div class="text-center">
        <h2 class="mt-6 text-3xl font-extrabold text-gray-900">Login</h2>
      </div>
      <p v-if="errorMessage" class="mt-2 text-center text-sm text-red-600">
        {{ errorMessage }}
      </p>
      <button @click="loginWithMicrosoft" class="w-full flex items-center justify-center p-4 bg-indigo-600 text-white rounded-full shadow-lg">
        <span v-if="isLoading">Loading...</span>
        <span v-else>Microsoft Login</span>
      </button>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import * as msal from '@azure/msal-browser';

const router = useRouter();

const isLoading = ref(false);
const errorMessage = ref('');

const msalConfig = {
  auth: {
    clientId: import.meta.env.VITE_CLIENT_ID,
    authority: import.meta.env.VITE_AUTHORIZATION_URL,
    redirectUri: import.meta.env.VITE_REDIRECT_URI,
  },
  cache: {
    cacheLocation: 'localStorage',
    storeAuthStateInCookie: false,
  },
};

const loginRequest = {
    scopes: ['Files.Read'],
  };

  
const msalInstance = new msal.PublicClientApplication(msalConfig);

onMounted(async () => {
  await msalInstance.initialize();
});

async function loginWithMicrosoft() {
  isLoading.value = true;
  errorMessage.value = '';

  try {
    const response = await msalInstance.loginPopup(loginRequest);

    const account = response.account;

    // Access Token für API abrufen
    const tokenResponse = await msalInstance.acquireTokenSilent({
      scopes: ['Files.Read'],
      account: account
    });

    const accessToken = tokenResponse.idToken;
  
    // Token speichern
    localStorage.setItem('accessToken', accessToken);
    localStorage.setItem('email', account.username);

    router.push('/'); // Weiterleitung zur Startseite
  } catch (error) {
    console.error('Login fehlgeschlagen:', error);
    errorMessage.value = 'Login fehlgeschlagen. Bitte versuche es erneut.';
  } finally {
    isLoading.value = false;
  }
}

</script>
