<script setup lang="ts">
import AppMain from '@/components/AppMain.vue';
defineProps({
  listId: {
    type: String,
    required: true,
  },
});
</script>

<template>
  <AppMain>
    <h1>List Detail View</h1>
    <p>listId: {{ listId }}</p>
  </AppMain>
</template>
