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
// import { login } from '../services/authService.js'; // Importiere die login-Funktion

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
console.log('MSAL Config:', msalConfig);
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

    console.log('Login erfolgreich', response);
    const account = response.account;

    // Access Token für API abrufen
    const tokenResponse = await msalInstance.acquireTokenSilent({
      scopes: ['Files.Read'],
      account: account
    });

    const accessToken = tokenResponse.accessToken;
    
    console.log('Decoded Access Token:', JSON.parse(atob(accessToken.split('.')[1])));
    console.log('API Token:', accessToken);

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




// function getAccount(msalInstance) {
//     const accounts = msalInstance.getAllAccounts();
//     return accounts.length > 0 ? accounts[0] : null;
//   }

// function getProfile(msalInstance) {
// const account = getAccount(msalInstance);
// if (account) {
//     msalInstance.acquireTokenSilent({
//     ...loginRequest,
//     account: account
//     }).then(response => {
//     console.log('Token erhalten:', response.accessToken);
//     const account = response.account;
//         const token = response.accessToken;
//         const email = account.username;
//         console.log('Token:', token);
//         console.log('Email:', email);
//         localStorage.setItem('accessToken', token);
//         localStorage.setItem('email', email);

//     }).catch(error => {
//     console.error('Fehler bei der Token-Anfrage:', error);
//     });
// }
// }


function logout(msalInstance) {
  msalInstance.logout();
  
  localStorage.removeItem('token');
  localStorage.removeItem('email');
}

</script>
