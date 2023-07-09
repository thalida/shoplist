<script setup lang="ts">
import { computed, ref } from 'vue';
import type { CallbackTypes } from "vue3-google-login";
import { useUserStore } from '@/stores/user';

const userStore = useUserStore()


const isAuthenticated = computed(() => {
  return userStore.isAuthenticated;
});
const handleLoginWithGoogle: CallbackTypes.TokenResponseCallback = (response) => {
  userStore.loginWithGoogle(response.access_token)
};
</script>

<template>
  <div class="flex flex-row space-x-4">
    <button v-if="isAuthenticated" @click="userStore.logout">Logout</button>
    <GoogleLogin v-else :callback="handleLoginWithGoogle" popup-type="TOKEN">
      <button>Signup with Google</button>
    </GoogleLogin>
  </div>
</template>

<style scoped>
</style>
