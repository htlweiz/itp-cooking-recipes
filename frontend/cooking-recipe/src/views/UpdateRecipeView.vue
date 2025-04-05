<template>
    <UpdateRecipe :id="id" />
</template>

<script setup>
import { defineProps } from 'vue';
import UpdateRecipe from '../components/UpdateRecipe.vue';

const props = defineProps({ id: null });
</script>
