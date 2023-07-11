<script setup lang="ts">
defineProps({
  enableSpacing: {
    type: Boolean,
    default: true,
  },
  enableFullHeight: {
    type: Boolean,
    default: false,
  },
})
</script>

<template>
  <main
    class="lg:pl-72"
    :class="{
      'py-10': enableSpacing,
      'h-screen': enableFullHeight,
    }"
  >
    <div
      :class="{
        'px-4 sm:px-6 lg:px-8': enableSpacing,
        'h-full': enableFullHeight,
      }"
    >
      <slot />
    </div>
  </main>
</template>

<style scoped>

</style>
