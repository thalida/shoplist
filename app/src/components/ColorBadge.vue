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
  showRemoveButton: {
    type: Boolean,
    required: false,
    default: false,
  },
});

const emit = defineEmits<{
  (e: 'remove'): void
}>()
</script>

<template>
  <div
    class="inline-flex items-center gap-x-1.5 rounded-md px-2 py-1 text-sm font-medium"
    :class="{
      'bg-white text-gray-600 ring-1 ring-gray-300 ring-inset': color === 'white',
      'bg-gray-200 text-gray-600': color === 'gray',
      'bg-orange-100 text-orange-700': color === 'orange',
      'bg-orange-800 text-orange-200': color === 'brown',
      'bg-slate-900 text-white': color === 'black',
      'bg-red-50 text-red-700': color === 'red',
      'bg-yellow-50 text-yellow-800': color === 'yellow',
      'bg-green-50 text-green-700': color === 'green',
      'bg-blue-50 text-blue-700': color === 'blue',
      'bg-purple-50 text-purple-700': color === 'purple',
      'bg-pink-50 text-pink-700': color === 'pink',
    }"
  >
    {{ label }}

    <button
      v-if="showRemoveButton"
      @click="emit('remove')"
      type="button"
      class="group relative -mr-1 h-3.5 w-3.5 rounded-sm hover:bg-gray-500/20"
      :class="{
        'hover:bg-gray-400/40': color === 'white' || color === 'gray',
        'hover:bg-orange-400/40': color === 'orange',
        'hover:bg-orange-950/40': color === 'brown',
        'hover:bg-slate-400/40': color === 'black',
        'hover:bg-red-400/40': color === 'red',
        'hover:bg-yellow-400/40': color === 'yellow',
        'hover:bg-green-400/40': color === 'green',
        'hover:bg-blue-400/40': color === 'blue',
        'hover:bg-purple-400/40': color === 'purple',
        'hover:bg-pink-400/40': color === 'pink',
      }"
    >
      <span class="sr-only">Remove</span>
      <svg
        viewBox="0 0 14 14"
        class="h-3.5 w-3.5"
        :class="{
          'stroke-gray-600': color === 'white' || color === 'gray',
          'stroke-orange-200': color === 'brown',
          'stroke-orange-700': color === 'orange',
          'stroke-white': color === 'black',
          'stroke-red-700': color === 'red',
          'stroke-yellow-800': color === 'yellow',
          'stroke-green-700': color === 'green',
          'stroke-blue-700': color === 'blue',
          'stroke-purple-700': color === 'purple',
          'stroke-pink-700': color === 'pink',
        }"
      >
        <path d="M4 4l6 6m0-6l-6 6" />
      </svg>
      <span class="absolute -inset-1" />
    </button>
  </div>
</template>

<style scoped>

</style>
