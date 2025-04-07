<template>
    <div class="min-h-screen bg-gray-100 flex items-center justify-center py-12 px-4 sm:px-6 lg:px-8">
        <div class="max-w-2xl w-full space-y-8 bg-white p-10 rounded-xl shadow-md">
            <div class="flex justify-between items-center">
                <router-link :to="`/recipe/${recipeId}`" class="text-indigo-600 hover:text-indigo-800 focus:outline-indigo-500">
                    <ArrowLeftIcon color="black" class="h-8 w-8" />
                </router-link>
                <div>
                    <h2 class="text-center text-3xl font-extrabold text-gray-900">Rezept bearbeiten</h2>
                    <p class="mt-2 text-center text-sm text-gray-600">
                        Aktualisieren Sie die Details Ihres Rezepts
                    </p>
                </div>
                <div class="w-8"></div>
            </div>
            <form @submit.prevent="updateRecipe" class="mt-8 space-y-6">
                <div class="space-y-4">
                    <div>
                        <label for="title" class="block text-lg font-medium text-gray-900">Titel</label>
                        <input id="title" type="text" v-model="recipe.title" placeholder="Titel des Rezepts" required
                        class="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-indigo-500"
                        />
                    </div>
                    <div>
                        <label for="description" class="block text-lg font-medium text-gray-900">Beschreibung</label>
                        <textarea id="description" required v-model="recipe.description" rows="3" placeholder="Kurze Beschreibung des Rezepts..."
                        class="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-indigo-500"
                        ></textarea>
                    </div>
                </div>
                <div class="space-y-4">
                    <h3 class="text-lg font-medium text-gray-900">Zutaten</h3>
                    <div v-for="(ingredient, index) in recipe.ingredients" :key="index" class="flex flex-col sm:flex-row gap-4">
                        <div class="flex-1">
                            <select v-model="ingredient.id" class="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-indigo-500" required>
                                <option value="" disabled>Zutat auswählen</option>
                                <option v-for="availableIngredient in getFilteredIngredients(index)" :value="availableIngredient.id" :key="availableIngredient.id" >
                                    {{ availableIngredient.name }}
                                </option>
                            </select>
                        </div>
                        <div class="w-full sm:w-24">
                            <input type="number" v-model="ingredient.amount" placeholder="Menge" min="0"
                                class="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-indigo-500"
                            />
                        </div>
                        <div class="w-full sm:w-24">
                            <select v-model="ingredient.unit" class="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md 
                            shadow-sm focus:outline-indigo-500" >
                                <option value="g">g</option>
                                <option value="kg">kg</option>
                                <option value="ml">ml</option>
                                <option value="l">l</option>
                                <option value="Stück">Stück</option>
                            </select>
                        </div>
                        <button type="button" @click="removeIngredient(index)" class="mt-1 p-2 text-red-600 hover:text-red-800 focus:outline-indigo-500">
                            <TrashIcon class="h-5 w-5" />
                        </button>
                    </div>
                    <button type="button" @click="addIngredient" class="inline-flex items-center px-4 py-2 border border-gray-300 rounded-md shadow-sm text-sm 
                    font-medium text-gray-700 bg-white hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500">
                        <PlusIcon class="h-5 w-5 mr-2" />
                        Zutat hinzufügen
                    </button>
                </div>
                <div class="space-y-4">
                    <h3 class="text-lg font-medium text-gray-900">Zubereitungsschritte</h3>
                    <div v-for="(step, index) in recipe.steps" :key="index" class="flex flex-col sm:flex-row gap-4">
                        <div class="w-full sm:w-16 flex items-center justify-start sm:justify-center">
                            <span class="text-lg font-medium text-gray-500">{{ index + 1 }}.</span>
                        </div>
                        <div class="flex-1">
                            <label :for="'step-' + index" class="sr-only">Schritt</label>
                            <textarea :id="'step-' + index" v-model="step.instruction" rows="2" :placeholder="'Schritt ' + (index + 1)"
                                class="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-indigo-500"
                            ></textarea>
                        </div>
                        <div class="flex items-start space-x-2">
                            <button type="button" @click="moveStep(index, -1)" :disabled="index === 0"
                                class="p-2 text-gray-600 hover:text-gray-800 disabled:opacity-50"
                            >
                                <ArrowUpIcon class="h-5 w-5" />
                            </button>
                            <button type="button" @click="moveStep(index, 1)" :disabled="index === recipe.steps.length - 1"
                                class="p-2 text-gray-600 hover:text-gray-800 disabled:opacity-50"
                            >
                                <ArrowDownIcon class="h-5 w-5" />
                            </button>
                            <button type="button" @click="removeStep(index)" class="p-2 text-red-600 hover:text-red-800 focus:outline-indigo-500">
                                <TrashIcon class="h-5 w-5" />
                            </button>
                        </div>
                    </div>
                    <button type="button" @click="addStep" class="inline-flex items-center px-4 py-2 border border-gray-300 rounded-md shadow-sm text-sm font-medium 
                    text-gray-700 bg-white hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500"
                    >
                        <PlusIcon class="h-5 w-5 mr-2" />
                        Schritt hinzufügen
                    </button>
                </div>
                <div>
                    <button type="submit" class="w-full flex justify-center py-2 px-4 border border-transparent rounded-md shadow-sm text-sm font-medium 
                    text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500"
                    >
                        Rezept aktualisieren
                    </button>
                </div>
            </form>
        </div>
    </div>
</template>
  
<script setup>
import { ref, onMounted } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import { PlusIcon, TrashIcon, ArrowUpIcon, ArrowDownIcon, ArrowLeftIcon } from 'lucide-vue-next';
import recipeService  from '../services/recipeService.js';

const route = useRoute();
const router = useRouter();
const recipeId = route.params.id;

const recipe = ref({
    title: '',
    description: '',
    ingredients: [{ id: null, name:'', amount: 0, unit: 'g' }],
    steps: [{ instruction: '' }]
});

const originalSteps = ref([]);
const originalIngredients = ref([]);

const availableIngredients = ref([])

const ingredientRecipes = ref([
    {
        id: Number,
        amount: Number,
        unit: '',
        related_recipe_id: Number,
        related_ingredient_id: Number
    }
]);

onMounted(async () => {
    try {
        const ingredientResponse = await recipeService.getIngredients()
        availableIngredients.value = ingredientResponse.data

        const response = await recipeService.getRecipe(recipeId);
        recipe.value = response.data;
        const allRelations = (await recipeService.getRecipeIngredients()).data;
        ingredientRecipes.value = allRelations.filter(ir => ir.related_recipe_id === Number(recipeId));

        recipe.value.ingredients = recipe.value.ingredients.map(ingredient => {
        const match = availableIngredients.value.find(item => item.name === ingredient.name);
        const relation = ingredientRecipes.value.find(ir => ir.related_ingredient_id === match?.id);

        return {
            ...ingredient,
            id: match ? match.id : null,
            relationId: relation ? relation.id : null 
        };
        });
        originalSteps.value = [...recipe.value.steps];
        originalIngredients.value = [...recipe.value.ingredients];
    } catch (error) {
        console.error('Failed to fetch recipe:', error);
    }

});

function addIngredient() {
  recipe.value.ingredients.push({ id: null, name: '', amount: '', unit: 'g' });
}

function removeIngredient(index) {
  recipe.value.ingredients.splice(index, 1);
  if (recipe.value.ingredients.length === 0) {
    addIngredient();
  }
}

function getFilteredIngredients(currentIndex) {
  const selectedIngredientIds = recipe.value.ingredients
    .filter((_, index) => index !== currentIndex)
    .map(ingredient => ingredient.id);

  return availableIngredients.value.filter(
    ingredient => !selectedIngredientIds.includes(ingredient.id)
  );
}

function addStep() {
  recipe.value.steps.push({ instruction: '' });
}

function removeStep(index) {
  recipe.value.steps.splice(index, 1);
  if (recipe.value.steps.length === 0) {
    addStep();
  }
}

function moveStep(index, direction) {
  const newIndex = index + direction;
  if (newIndex >= 0 && newIndex < recipe.value.steps.length) {
    const steps = recipe.value.steps;
    [steps[index], steps[newIndex]] = [steps[newIndex], steps[index]];
  }
}

async function updateRecipe() {
    const updatedRecipe = {
        ...recipe.value,
        updated_at: new Date().toISOString(),
        steps: recipe.value.steps
        .filter(step => step.instruction.trim() !== '')
        .map((step, index) => ({
            ...step,
            step_number: index + 1
        }))
    };

    const validIngredients = updatedRecipe.ingredients.filter(ingredient => ingredient.id);
    const updatedIngredientIds = validIngredients.map(ing => ing.id);

    const originalStepIds = originalSteps.value.map(step => step.id).filter(Boolean);
    const updatedStepIds = updatedRecipe.steps.map(step => step.id).filter(Boolean);
    const stepsToDelete = originalStepIds.filter(id => !updatedStepIds.includes(id));

    await recipeService.updateRecipe(recipeId, {
        title: updatedRecipe.title,
        description: updatedRecipe.description
    });

    for (const ingredient of validIngredients) {
        if (!ingredient.relationId) {
            await recipeService.createRecipeIngredient({
                amount: ingredient.amount,
                unit: ingredient.unit,
                related_recipe_id: recipeId,
                related_ingredient_id: ingredient.id
            });
        } else {
            await recipeService.updateRecipeIngredient(ingredient.relationId, {
                amount: ingredient.amount,
                unit: ingredient.unit
            });
        }
    }

    const relationsToDelete = ingredientRecipes.value.filter(
        ir => !updatedIngredientIds.includes(ir.related_ingredient_id)
    );

    for (const rel of relationsToDelete) {
        await recipeService.deleteRecipeIngredient(rel.id);
    }

    for (const stepId of stepsToDelete) {
        await recipeService.deleteStep(stepId);
    }

    for (const step of updatedRecipe.steps) {
        if (!step.id) {
        const newStep = await recipeService.createStep({
            instruction: step.instruction,
            step_number: step.step_number,
            related_recipe_id: recipeId,
            title: 'Titel',
        });
        step.id = newStep.data.id;
        } else {
        await recipeService.updateStep(step.id, {
            instruction: step.instruction,
            step_number: step.step_number
        });
        }
    }

    router.push(`/recipe/${recipeId}`);
}

</script>
