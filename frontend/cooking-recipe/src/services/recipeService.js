import axios from 'axios';
import { isAuthenticated } from './userService';
import { apiClient } from './apiClient';

const formatParams = (params) => {
    const searchParams = new URLSearchParams();
    Object.entries(params).forEach(([key, value]) => {
        if (Array.isArray(value)) {
            value.forEach((val) => searchParams.append(key, val));
        } else if (value !== null && value !== undefined) {
            searchParams.append(key, value);
        }
    });
    return searchParams.toString();
};

export default {
    getRecipes(params) {
        return apiClient.get(`/recipes/?${formatParams(params)}`);
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
    getIngredients(params) {
        return apiClient.get(`/ingredients/${formatParams(params)}`);
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
    getSteps(params) {
        return apiClient.get(`/steps/${formatParams(params)}`);
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
    getRecipeIngredients(recipeId, params) {
        return apiClient.get(`/recipes/${recipeId}/ingredients${formatParams(params)}`);
    },
    createRecipeIngredient(amount, unit, ingredientId, recipeId) {
        return apiClient.post(`ingredients_recipe`, amount, unit, ingredientId, recipeId);
    },
    getRecipeSteps(recipeId) {
        return apiClient.get(`/recipes/${recipeId}/steps`);
    },
    getStars(params) {
        return apiClient.get(`/stars/${formatParams(params)}`);
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
  
