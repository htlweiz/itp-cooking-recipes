<template>
    <div>
        <div class="bg-white shadow overflow-hidden sm:rounded-lg">
            <div class="px-4 py-5 sm:px-6">
                <h3 class="text-lg font-medium leading-6 text-gray-900">Recipe Details</h3>
                <p class="mt-1 max-w-text-sm text-gray-500">Details and information about the recipe.</p>
                {{ props.id }}
            </div>
        </div>
    </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';

const props = defineProps({ id: Number });

onMounted(() => {
    console.log('Recipe ID:', props.id);
});
</script>