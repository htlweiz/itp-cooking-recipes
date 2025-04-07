<template>
    <RecipeDetail :id="id" />
</template>

<script setup>
import { defineProps } from 'vue';
import RecipeDetail from '../components/RecipeDetail.vue';

const props = defineProps({ id: null });
</script>
