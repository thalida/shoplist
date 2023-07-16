<script setup lang="ts">
import { useRouter } from 'vue-router';
import { XIcon } from 'lucide-vue-next';
import { DialogTitle } from '@headlessui/vue';
import { PRODUCTS_ROUTE } from '@/router';
import { useProductStore } from '@/stores/product';
import { computed, onMounted } from 'vue';


const props = defineProps({
  productId: {
    type: String,
    required: true,
  },
});
const router = useRouter();
const productStore = useProductStore();
const product = computed(() => productStore.getById(props.productId));

function handleDetailPanelClose() {
  router.push({
    name: PRODUCTS_ROUTE,
    params: {
      productId: null,
    },
  });
}

onMounted(() => {
  productStore.getOrFetch(props.productId);
});
</script>

<template>
  <div class="flex flex-col h-full">
    <div class="p-4 sm:p-6 flex flex-shrink-0">
      <div class="flex items-start justify-between w-full">
        <DialogTitle class="text-base font-semibold leading-6 text-gray-900">
          {{ product.name }}
        </DialogTitle>
        <div class="ml-3 flex h-7 items-center">
          <button type="button" class="rounded-md bg-white text-gray-400 hover:text-gray-500 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:ring-offset-2" @click="handleDetailPanelClose">
            <span class="sr-only">Close panel</span>
            <XIcon class="h-6 w-6" aria-hidden="true" />
          </button>
        </div>
      </div>
    </div>
    <div class="relative mt-6 flex-grow px-4 sm:px-6 overflow-auto">
      {{ product }}
    </div>
    <div class="flex flex-shrink-0 justify-end p-4 sm:p-6 border-t border-gray-200">
      <button type="button">Delete</button>
      <button type="button" class="rounded-md bg-white px-3 py-2 text-sm font-semibold text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 hover:ring-gray-400" @click="open = false">Cancel</button>
      <button type="submit" class="ml-4 inline-flex justify-center rounded-md bg-indigo-600 px-3 py-2 text-sm font-semibold text-white shadow-sm hover:bg-indigo-500 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-indigo-500">Save</button>
    </div>
  </div>
</template>
