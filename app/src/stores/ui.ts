import { ref } from 'vue'
import { defineStore } from 'pinia'

export const useUiStore = defineStore('ui', () => {
  const isSidebarOpen = ref(false)

  function toggleSidebar() {
    isSidebarOpen.value = !isSidebarOpen.value
  }

  function closeSidebar() {
    isSidebarOpen.value = false
  }

  function openSidebar() {
    isSidebarOpen.value = true
  }

  return {
    isSidebarOpen,
    toggleSidebar,
    closeSidebar,
    openSidebar
  }
})
