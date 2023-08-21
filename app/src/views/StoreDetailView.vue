<script setup lang="ts">
import AppMain from '@/components/AppMain.vue';
defineProps({
  storeId: {
    type: String,
    required: true,
  },
});
</script>

<template>
  <AppMain>
    <h1>Store Detail View</h1>
    <p>Store: {{ storeId }}</p>
  </AppMain>
</template>
