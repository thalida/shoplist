<script setup lang="ts">
import AppMain from '@/components/AppMain.vue';
import AuthButton from '@/components/AuthButton.vue';
</script>

<template>
  <AppMain :enableSpacing="false" :enable-full-height="true">
    <div class="signin-view flex min-h-full flex-1">
      <div class="flex flex-1 flex-col justify-center px-4 py-12 sm:px-6 lg:flex-none lg:px-20 xl:px-24">
        <div class="mx-auto w-full max-w-sm lg:w-96">
          <div>
            <h2 class="mt-8 text-2xl font-bold leading-9 tracking-tight text-gray-900">Sign in to your account</h2>
          </div>

          <AuthButton class="w-full max-w-64" />
        </div>
      </div>
      <div class="relative hidden w-0 flex-1 lg:block">
        <img class="absolute inset-0 h-full w-full object-cover" src="https://images.unsplash.com/photo-1496917756835-20cb06e75b4e?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=1908&q=80" alt="" />
      </div>
    </div>
  </AppMain>
</template>

<style scoped>
.signin-view {
  height: 100%;
}
</style>
