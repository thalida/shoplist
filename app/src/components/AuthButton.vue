<script setup lang="ts">
import type { CallbackTypes } from "vue3-google-login";
import { useUserStore } from '@/stores/user';
import IconGoogle from "@/components/icons/IconGoogle.vue";
import { useRouter } from "vue-router";
import { HOME_ROUTE } from "@/router";

defineProps({
  theme: {
    type: String,
    default: 'dark',
    options: ['dark', 'light'],
  },
})

const router = useRouter();
const userStore = useUserStore()
// const handleLoginWithGoogle: CallbackTypes.TokenResponseCallback = (response) => {
//   userStore.loginWithGoogle(response.access_token)
// };

const handleLoginWithGoogle: CallbackTypes.TokenResponseCallback = (response) => {
  userStore
    .loginWithSocial({ socialAccessToken: response.access_token, socialBackend: "google-oauth2" })
    .then(handleResponse);
};
function handleResponse() {
  if (userStore.isAuthenticated) {
    router.push({ name: HOME_ROUTE });
  }
}
</script>

<template>
  <GoogleLogin :callback="handleLoginWithGoogle" popup-type="TOKEN">
    <button
      class="w-full flex flex-row items-center justify-center gap-3 rounded-md px-3 py-1.5 text-sm focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2"
      :class="{
        'bg-gray-900 focus-visible:outline-gray-900 text-white': theme === 'dark',
        'bg-white focus-visible:outline-white text-gray-950': theme === 'light',
      }"
    >
      <IconGoogle class="h-5 w-5" aria-hidden="true" />
      <span>Sign in with Google</span>
    </button>
  </GoogleLogin>
</template>

<style scoped>
</style>
