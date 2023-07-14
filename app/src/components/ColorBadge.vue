<script setup lang="ts">
defineProps({
  label: {
    type: String,
    required: true,
  },
  color: {
    type: String,
    default: 'gray',
  },
});
</script>

<template>
  <div
    class="inline-flex items-center rounded-md ring-1 ring-inset px-2 py-1 text-xs font-medium"
    :class="{
      'bg-white text-gray-600 ring-gray-300': color === 'white',
      'bg-gray-50 text-gray-600 ring-gray-500/10': color === 'gray',
      'bg-orange-800 text-orange-200 ring-orange-900': color === 'brown',
      'bg-slate-900 text-white ring-black/10': color === 'black',
      'bg-red-50 text-red-700 ring-red-600/10': color === 'red',
      'bg-yellow-50 text-yellow-800 ring-yellow-600/20': color === 'yellow',
      'bg-green-50 text-green-700 ring-green-600/20': color === 'green',
      'bg-blue-50 text-blue-700 ring-blue-700/10': color === 'blue',
      'bg-purple-50 text-purple-700 ring-purple-700/10': color === 'purple',
      'bg-pink-50 text-pink-700 ring-pink-700/10': color === 'pink',
    }"
  >
    {{ label }}
  </div>
</template>

<style scoped>

</style>
