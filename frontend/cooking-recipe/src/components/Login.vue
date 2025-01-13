<template>
    <div class="login-container">
        <div class = "login-header">
            <h1>Login</h1>
        </div>
        <form @submit.prevent="handleSubmit" class="login-form">
            <div class="form-group">
                <label for="email">Email</label>
                <input type="email" class="form-control" id="email" aria-describedby="emailHelp" placeholder="Enter email" v-model="email">
            </div>
            <div class="form-group">
                <label for="password">Password</label>
                <div class="password-input">
                    <input :type="showPassword ? 'text' : 'password'" id="password" v-model="password" placeholder="password" required>
                    <button type="button" @click="togglePassword" class="password-toggle">{{ showPassword ? 'Hide' : 'Show' }}</button>
                </div>
            </div>
            <button type="submit" class="login-button" :disabled="isLoading">
                {{ isLoading ? 'Logging in...' : 'Log In' }}
            </button>
        </form>
    </div>
</template>

<script setup>
import { ref } from 'vue';

const email = ref('');
const password = ref('');
const showPassword = ref(false);
const isLoading = ref(false);
const errorMessage = ref('');

function togglePassword() {
  showPassword.value = !showPassword.value;
}
function handleSubmit() {
    console.log('Email:', email.value);
    console.log('Password:', password.value);
}
</script>

<style scoped>
.login-container {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 1rem;
}

</style>
  