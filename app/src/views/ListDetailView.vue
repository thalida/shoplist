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
  Lists Detail View {{ listId }}
</template>
