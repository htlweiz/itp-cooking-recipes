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
    getRecipes(params = {page: 0, page_size: 100000}) {
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
    getRecipePic(recipeId) {
        return apiClient.get(`/recipes/${recipeId}/pic/`, {
            responseType: 'blob',
        });
    },
    uploadRecipePic(recipeId, formData) {
        return apiClient.post(`/recipes/${recipeId}/upload_pic/`, formData, {
          headers: {
            'Content-Type': 'multipart/form-data',
          },
        });
      },
    getIngredients(params = {page: 0, page_size: 100000}) {
        return apiClient.get(`/ingredients/?${formatParams(params)}`);
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
    getRecipeIngredients(params = {page: 0, page_size: 100000}) {
        return apiClient.get(`/ingredients_recipes/?${formatParams(params)}`);
    },
    createRecipeIngredient(recipeIngredient) {
        return apiClient.post('/ingredients_recipes/', recipeIngredient);
    },
    updateRecipeIngredient(id, recipeIngredient) {
        return apiClient.put(`/ingredients_recipes/${id}`, recipeIngredient);
    },
    deleteRecipeIngredient(id) {
        return apiClient.delete(`/ingredients_recipes/${id}`);
    },
    getRecipeSteps(recipeId) {
        return apiClient.get(`/recipes/${recipeId}/steps`);
    },
    getStars(params = {page: 0, page_size: 100000}) {
        return apiClient.get(`/stars/?${formatParams(params)}`);
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
  
