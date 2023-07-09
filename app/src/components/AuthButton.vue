<script setup lang="ts">
import { computed, ref } from 'vue';
import type { CallbackTypes } from "vue3-google-login";
import { PowerIcon } from '@heroicons/vue/24/outline'
import { useUserStore } from '@/stores/user';
import { getFullName } from '@/utils/user';
import UserAvatar from '@/components/UserAvatar.vue';

const userStore = useUserStore()
const myFullName = computed(() => {
  return userStore.me ? getFullName(userStore.me) : null
})

const isAuthenticated = computed(() => {
  return userStore.isAuthenticated;
});
const handleLoginWithGoogle: CallbackTypes.TokenResponseCallback = (response) => {
  userStore.loginWithGoogle(response.access_token)
};
</script>

<template>
  <div class="flex flex-row space-x-4">
    <div v-if="isAuthenticated && userStore.me" class="w-full flex flex-row items-center justify-between gap-x-4 py-3">
      <div class="flex flex-row items-center gap-x-4 text-sm font-semibold leading-6 text-white">
        <UserAvatar :user="userStore.me" />
        <span aria-hidden="true">{{ myFullName }}</span>
      </div>
      <button @click="userStore.logout" type="button" class="rounded-full bg-gray-800 p-1.5 text-white shadow-sm hover:bg-gray-600 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-gray-600">
        <PowerIcon class="h-5 w-5" aria-hidden="true" />
      </button>
    </div>
    <GoogleLogin v-else :callback="handleLoginWithGoogle" popup-type="TOKEN">
      <button>Signin with Google</button>
    </GoogleLogin>
  </div>
</template>

<style scoped>
</style>
