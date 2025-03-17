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
        Microsoft Login
      </button>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import * as msal from '@azure/msal-browser';  // MSAL importieren
import { login } from '../services/userService.js';  // Die Funktion zum Speichern von Token und E-Mail

const router = useRouter();

const isLoading = ref(false);
const errorMessage = ref('');

const msalConfig = {
  auth: {
    clientId: import.meta.env.VITE_CLIENT_ID,  // Deine Client-ID
    authority: import.meta.env.VITE_AUTHORIZATION_URL,  // Deine Tenant-ID
    redirectUri: import.meta.env.VITE_REDIRECT_URI,  // Deine Redirect-URI
  },
  cache: {
    cacheLocation: "localStorage",  // Wählen, wo das Token gespeichert werden soll
    storeAuthStateInCookie: false,  // Verhindert Auth-Fehler in IE
  },
};

const msalInstance = new msal.PublicClientApplication(msalConfig);

// Funktion zum Überprüfen, ob der Benutzer bereits eingeloggt ist
async function checkAccount() {
  const accounts = msalInstance.getAllAccounts();
  console.log('Accounts:', accounts);
  if (accounts.length > 0) {
    console.log('Benutzer bereits eingeloggt:', accounts[0]);
    router.push('/');
    return true;
  }
  return false;
}

// Prüft beim Laden der Seite, ob ein Redirect erfolgt ist
onMounted(async () => {
  await msalInstance.initialize();  // Initialisiere MSAL
  const result = await msalInstance.handleRedirectPromise();  // Handle redirect promise nach Login
  if (result) {
    console.log('Login nach Redirect erfolgreich:', result);
    msalInstance.setActiveAccount(result.account);  // Setze das aktive Konto
    await handleLoginSuccess(result);  // Bearbeite den Login
  }
});

async function loginWithMicrosoft() {
  if (isLoading.value) {
    return;
  }

  const alreadyLoggedIn = await checkAccount();
  if (alreadyLoggedIn) {
    return;
  }

  try {
    isLoading.value = true;

    // Starte die Login-Popup-Anforderung
    const loginResponse = await msalInstance.loginPopup({
      scopes: [`${import.meta.env.VITE_SCOPE}`],  // Hier deine Scopes einfügen
    });

    // Nach erfolgreichem Login, handle den Login
    await handleLoginSuccess(loginResponse);
  } catch (error) {
    console.error('Login fehlgeschlagen:', error);
    errorMessage.value = 'Microsoft Login fehlgeschlagen';
  } finally {
    isLoading.value = false;
  }
}

// Verarbeitung des erfolgreichen Logins
async function handleLoginSuccess(loginResponse) {
  try {
    const account = msalInstance.getActiveAccount();
    if (account) {
      console.log('Benutzer erfolgreich eingeloggt:', account);

      // Abrufen des Access Tokens für den authentifizierten Benutzer
      const tokenResponse = await msalInstance.acquireTokenSilent({
        scopes: [`${import.meta.env.VITE_SCOPE}`],
        account: account,
      });

      console.log('Access Token:', tokenResponse.accessToken);

      // Speichern des Tokens und der E-Mail-Adresse im LocalStorage
      login(tokenResponse.accessToken, account.username);  // Speichern des Tokens und der E-Mail

      // Weiterleitung zur Startseite nach erfolgreichem Login
      router.push('/');
    }
  } catch (error) {
    console.error('Fehler beim Abrufen des Tokens:', error);
    errorMessage.value = 'Fehler beim Abrufen des Tokens. Bitte versuche es erneut.';
  }
}
</script>
