<script setup lang="ts">
import type { IUser } from '@/types/user';
import { computed, type PropType } from 'vue';

const props = defineProps({
  user: {
    type: Object as PropType<IUser>,
    required: true,
  },
})

const initials = computed(() => {
  return props.user.first_name[0] + props.user.last_name[0];
})
</script>

<template>
  <div>
    <img v-if="user.avatar" class="inline-block h-8 w-8 rounded-full bg-gray-800" :src="user.avatar" alt="" />
    <span v-else class="inline-flex h-8 w-8 items-center justify-center rounded-full bg-gray-800">
      <span class="text-sm font-medium leading-none text-white">{{  initials  }}</span>
    </span>
  </div>
</template>

<style scoped>

</style>
