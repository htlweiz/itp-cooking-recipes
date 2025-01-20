<template>
    <div>
        <h1>Rezept erstellen</h1>
        <div>
            <div>
                <label for="title">Titel:</label>
                <input type="text" id="title" v-model="recipe.title" />
            </div>
            <div>
                <label for="description">Beschreibung:</label>
                <textarea id="description" v-model="recipe.description"></textarea>
            </div>
            <div>
                <label for="ingredients">Zutaten:</label>
                <input type="text" id="ingredients" v-model="recipe.ingredients" />
            </div>
            <div>
                <label for="steps">Schritte:</label>
                <input type="text" id="steps" v-model="recipe.steps" />
            </div>
        </div>
    </div>
</template>


<script setup>
import { ref } from 'vue';

const recipe = ref({
    title: '',
    description: '',
    created_at: '',
    ingredients: [],
    steps: []
});
</script>