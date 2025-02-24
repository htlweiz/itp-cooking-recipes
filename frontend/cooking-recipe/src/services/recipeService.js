import axios from 'axios';
import { isAuthenticated } from './userService';
import { apiClient } from './apiClient';
  
export default {
    getRecipes() {
        return apiClient.get('/recipes/');
    },
    getRecipe(id) {
        return apiClient.get(`/recipes/${id}`);
    },
    createRecipe(recipe) {
        return apiClient.post('/recipes/', recipe);
    },
    updateRecipe(id, recipe) {
        return apiClient.put(`/recipes/${id}`, recipe);
    },
    deleteRecipe(id) {
        return apiClient.delete(`/recipes/${id}`);
    },
    getIngredients() {
        return apiClient.get('/ingredients/');
    },
    getIngredient(id) {
        return apiClient.get(`/ingredients/${id}`);
    },
    createIngredient(ingredient) {
        return apiClient.post('/ingredients/', ingredient);
    },
    updateIngredient(id, ingredient) {
        return apiClient.put(`/ingredients/${id}`, ingredient);
    },
    deleteIngredient(id) {
        return apiClient.delete(`/ingredients/${id}`);
    },
    getSteps() {
        return apiClient.get('/steps/');
    },
    getStep(id) {
        return apiClient.get(`/steps/${id}`);
    },
    createStep(step_number, instrution, title, recipeId) {
        return apiClient.post('/steps/', step_number, instrution, title, recipeId);
    },
    updateStep(id, step) {
        return apiClient.put(`/steps/${id}`, step);
    },
    deleteStep(id) {
        return apiClient.delete(`/steps/${id}`);
    },
    getRecipeIngredients(recipeId) {
        return apiClient.get(`/recipes/${recipeId}/ingredients`);
    },
    createRecipeIngredient(amount, unit, ingredientId, recipeId) {
        return apiClient.post(`ingredients_recipe`, amount, unit, ingredientId, recipeId);
    },
    getRecipeSteps(recipeId) {
        return apiClient.get(`/recipes/${recipeId}/steps`);
    },
    getStars() {
        return apiClient.get('/stars/');
    },
    getStar(id) {
        return apiClient.get(`/stars/${id}`);
    },
    createStar(star) {
        return apiClient.post('/stars/', star);
    },
    updateStar(id, star) {
        return apiClient.put(`/stars/${id}`, star);
    },
    deleteStar(id) {
        return apiClient.delete(`/stars/${id}`);
    },
    getAverageStarsPerRecipe(recipeId) {
        return apiClient.get(`/stars/${recipeId}/stars`);
    }
};
  
