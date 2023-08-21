<script setup lang="ts">
import { computed, onMounted, ref, type Ref } from 'vue';
import { useRouter } from 'vue-router';
import { XIcon } from 'lucide-vue-next';
import { cloneDeep, keyBy } from 'lodash';
import { DialogTitle } from '@headlessui/vue';
import { PRODUCTS_ROUTE } from '@/router';
import { useProductStore } from '@/stores/product';
import { useListStore } from '@/stores/list';
import { useStoreStore } from '@/stores/store';
import ComboboxFilter from '@/components/ComboboxFilter.vue';
import ColorBadge from '@/components/ColorBadge.vue';

const props = defineProps({
  productId: {
    type: String,
    required: true,
  },
});
const isCreateMode = computed(() => props.productId === 'new');
const router = useRouter();

const listStore = useListStore();
const storeStore = useStoreStore();
const productStore = useProductStore();

const categoriesComboxFilter: Ref<InstanceType<typeof ComboboxFilter> | null> = ref(null);

const product = ref({
  name: '',
  categories: [] as string[],
  lists: [] as string[],
  stores: [] as string[],
});

const title = computed(() => {
  if (isCreateMode.value) {
    return 'New Product';
  }
  return `Edit Product: ${product.value.name}`;
});

function handleDetailPanelClose() {
  router.push({
    name: PRODUCTS_ROUTE,
    params: {
      productId: null,
    },
  });
}

function handleFiltersChanged(field: string, selectedItems: string[]) {
  product.value[field] = selectedItems;
}

onMounted(async () => {
  await Promise.all([
    storeStore.fetch(),
    listStore.fetch(),
    productStore.fetchCategories(),
  ]);

  if (isCreateMode.value) {
    product.value.categories = cloneDeep(productStore.filterBy.categories)
  } else {
    await productStore.getOrFetch(props.productId);

    const dbProduct = productStore.getById(props.productId);

    if (dbProduct) {
      product.value = cloneDeep(dbProduct);
      product.value.categories = Object.keys(keyBy(dbProduct.categories, 'uid'));
    }
  }

});
</script>

<template>
  <div class="flex flex-col h-full">
    <div class="p-4 sm:p-6 flex flex-shrink-0">
      <div class="flex items-start justify-between w-full">
        <DialogTitle class="text-base font-semibold leading-6 text-gray-900">
          {{ title }}
        </DialogTitle>
        <div class="ml-3 flex h-7 items-center">
          <button type="button" class="rounded-md bg-white text-gray-400 hover:text-gray-500 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:ring-offset-2" @click="handleDetailPanelClose">
            <span class="sr-only">Close panel</span>
            <XIcon class="h-6 w-6" aria-hidden="true" />
          </button>
        </div>
      </div>
    </div>
    <div class="relative mt-6 flex-grow px-4 sm:px-6 overflow-auto space-y-6">
      <div class="space-y-2">
        <label for="first-name" class="block text-sm font-medium leading-6 text-gray-900">Product Name</label>
        <div>
          <input
            type="text"
            class="block w-full rounded-md border-0 py-1.5 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-indigo-600 sm:text-sm sm:leading-6"
            v-model="product.name"
          />
        </div>
      </div>
      <div class="space-y-2">
        <label for="first-name" class="block text-sm font-medium leading-6 text-gray-900">Categories</label>
        <ComboboxFilter
          ref="categoriesComboxFilter"
          :items="productStore.categories"
          :selected="product.categories"
          labelKey="name"
          valueKey="uid"
          idKey="uid"
          inputPlaceholder="Search categories"
          @update:selected="(items) => handleFiltersChanged('categories', items)"
        >
          <template #selected="{ selected }">
            <ColorBadge
              v-for="categoryUid in selected"
              :key="categoryUid"
              :label="productStore.getCategoryById(categoryUid)?.name"
              :color="productStore.getCategoryById(categoryUid)?.color"
              :showRemoveButton="true"
              @remove="categoriesComboxFilter?.removeItem(categoryUid)"
            />
          </template>
        </ComboboxFilter>
      </div>
    </div>
    <div class="flex flex-shrink-0 justify-end p-4 sm:p-6 border-t border-gray-200 space-x-2">
      <button
        type="button"
        class="rounded-md bg-red-600 px-3 py-2 text-sm font-semibold text-white shadow-sm ring-1 ring-inset ring-gray-300 hover:ring-gray-400"
        @click="handleDetailPanelClose"
      >
        Delete
      </button>
      <button
        type="button"
        class="rounded-md bg-white px-3 py-2 text-sm font-semibold text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 hover:ring-gray-400"
        @click="handleDetailPanelClose"
      >
        Cancel
      </button>
      <button
        type="submit"
        class="rounded-md bg-indigo-600 px-3 py-2 text-sm font-semibold text-white shadow-sm hover:bg-indigo-500 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-indigo-500"
        @click="handleDetailPanelClose"
      >
        Save
      </button>
    </div>
  </div>
</template>
