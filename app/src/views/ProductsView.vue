<script setup lang="ts">
import AppMain from '@/components/AppMain.vue';
import { useShopStore } from '@/stores/shop';

const shopStore = useShopStore();

shopStore.getProducts();
</script>

<template>
  <AppMain>
    Products View
  </AppMain>
</template>
