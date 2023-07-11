<script setup lang="ts">
import { onMounted, ref } from "vue";
import { RouterView } from 'vue-router'
import AppSidebar from './components/AppSidebar.vue'
import AppHeader from './components/AppHeader.vue'
import AppMain from './components/AppMain.vue'
import { useUserStore } from './stores/user';

const isLoading = ref(true);
const userStore = useUserStore();

onMounted(async () => {
  await userStore.autoLogin();
  isLoading.value = false
})
</script>

<template>
  <template v-if="isLoading">
    Loading &hellip;
  </template>
  <template v-else>
    <div>
      <AppHeader />
      <AppSidebar />
      <RouterView />
    </div>
  </template>
</template>
