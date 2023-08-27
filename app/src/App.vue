<script setup lang="ts">
import { onMounted, ref } from "vue";
import { RouterView } from 'vue-router'
import AppSidebar from './components/AppSidebar.vue'
import AppHeader from './components/AppHeader.vue'
import { useUserStore } from './stores/user';

const isLoading = ref(true);
const userStore = useUserStore();

const room = 'general'
const socket = new WebSocket('ws://127.0.0.1:8000/ws/chat/' + room + '/')
socket.onopen = function(e) {
  console.log('Connection established')
}
socket.onmessage = function(event) {
  console.log(event.data)
}
socket.onclose = function(event) {
  if (event.wasClean) {
    console.log('Connection closed')
  } else {
    console.log('Connection interrupted')
  }
  console.log('Code: ' + event.code + ' Reason: ' + event.reason)
}
socket.onerror = function(error) {
  console.log('Error: ' + error.message)
}
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
