<script setup lang="ts">
import { computed, onMounted, ref, type Ref } from 'vue';
import { useRouter } from 'vue-router';
import { XIcon } from 'lucide-vue-next';
import { cloneDeep, keyBy } from 'lodash';
import { DialogTitle } from '@headlessui/vue';
import { PRODUCTS_ROUTE } from '@/router';
import { useProductStore } from '@/stores/product';
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
const storeStore = useStoreStore();
const productStore = useProductStore();

const categoriesComboxFilter: Ref<InstanceType<typeof ComboboxFilter> | null> = ref(null);

const product = ref({
  uid: null as string | null,
  name: '',
  categories: [] as string[],
  stores: [] as any[],
});

const title = computed(() => {
  if (isCreateMode.value) {
    return 'New Product';
  }
  return `Edit Product: ${product.value.name}`;
});

const availableStores = computed(() => {
  return storeStore.collectionAsArray.filter((store) => {
    return !product.value.stores.find((storeProduct: any) => {
      return storeProduct.store === store.uid;
    });
  });
});

const totalStores = computed(() => {
  return storeStore.collectionAsArray.length;
});

const hasAllStores = computed(() => {
  return product.value.stores.length === totalStores.value;
});


function handleDetailPanelClose() {
  router.push({
    name: PRODUCTS_ROUTE,
    params: {
      productId: null,
    },
  });
}

function handleProductCancel() {
  handleDetailPanelClose();
}

async function handleProductDelete() {
  await productStore.remove({
    uid: props.productId,
  });
  await productStore.refetch();
  handleDetailPanelClose();
}

async function handleProductSave() {
  await productStore.createOrUpdate(product.value);
  productStore.refetch();
  handleDetailPanelClose();
}

function handleFiltersChanged(field: string, selectedItems: string[]) {
  product.value[field] = selectedItems;
}

function handleAddStore() {
  product.value.stores.push({
    store: null,
    section: null,
    price: null,
    shouldRemove: false
  });
}

onMounted(async () => {
  await Promise.all([
    storeStore.fetch(),
    productStore.fetchCategories(),
    productStore.fetchUnits(),
  ]);

  if (isCreateMode.value) {
    product.value.categories = cloneDeep(productStore.filterBy.categories)
  } else {
    await productStore.getOrFetch(props.productId);

    const dbProduct = productStore.getById(props.productId);

    if (dbProduct) {
      product.value = cloneDeep(dbProduct);
      product.value.categories = Object.keys(keyBy(dbProduct.categories, 'uid'));

      const productStores = [];
      for (const storeProduct of dbProduct.stores) {
        const formattedStoreProudct = {
          ...storeProduct,
          store: storeProduct.store.uid,
          section: storeProduct.section?.uid,
          shouldRemove: false,
        };

        productStores.push(formattedStoreProudct)
      }
      product.value.stores = productStores;
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
          :allowCustomValues="true"
        >
          <template #selected="{ selected }">
            <template v-for="category in selected" :key="category">
              <ColorBadge
                v-if="typeof category === 'string'"
                :label="productStore.getCategoryById(category)?.name"
                :color="productStore.getCategoryById(category)?.color"
                :showRemoveButton="true"
                @remove="categoriesComboxFilter?.removeItem(category)"
              />
              <ColorBadge
                v-else
                :label="category.name"
                :color="category.color"
                :showRemoveButton="true"
                @remove="categoriesComboxFilter?.removeItem(category)"
              />
            </template>
          </template>
        </ComboboxFilter>
      </div>
      <div class="space-y-2">
        <label class="col-span-3 block text-sm font-medium leading-6 text-gray-700">Assigned Stores</label>
        <div class="grid grid-cols-10 gap-2" v-if="product.stores.length > 0">
          <label class="col-span-3 block text-sm leading-6 text-gray-700">Store</label>
          <label class="col-span-3 block text-sm leading-6 text-gray-700">Section</label>
          <label class="col-span-3 block text-sm leading-6 text-gray-700">Price</label>
          <label class="block text-sm leading-6 text-red-500">Remove?</label>
        </div>
        <div
          v-for="storeProduct in product.stores"
          :key="storeProduct.id"
          class="grid grid-cols-10 gap-2 items-center"
        >
          <select
            :id="`storeproduct-${storeProduct.id}__store`"
            :name="`storeproduct-${storeProduct.id}__store`"
            v-model="storeProduct.store"
            class="col-span-3 block w-full rounded-md border-0 py-1.5 pl-3 pr-10 text-gray-900 ring-1 ring-inset ring-gray-300 focus:ring-2 focus:ring-indigo-600 sm:text-sm sm:leading-6"
          >
            <option value="">Select a store</option>
            <option v-if="storeProduct.store" :value="storeProduct.store">{{ storeStore.getById(storeProduct.store).name  }}</option>
            <option
              v-for="store in availableStores"
              :key="store.uid"
              :value="store.uid"
            >
              {{ store.name }}
            </option>
          </select>
          <select
            :disabled="storeStore.getById(storeProduct.store)?.sections.length === 0"
            :id="`storeproduct-${storeProduct.id}__section`"
            :name="`storeproduct-${storeProduct.id}__section`"
            v-model="storeProduct.section"
            class="col-span-3 block w-full rounded-md border-0 py-1.5 pl-3 pr-10 text-gray-900 ring-1 ring-inset ring-gray-300 focus:ring-2 focus:ring-indigo-600 sm:text-sm sm:leading-6"
          >
            <option value="">Select a section</option>
            <option
              v-for="section in storeStore.getById(storeProduct.store)?.sections"
              :key="section.uid"
              :value="section.uid"
            >
              {{ section.name }}
            </option>
          </select>
          <div class="col-span-3 relative rounded-md shadow-sm">
            <div class="pointer-events-none absolute inset-y-0 left-0 flex items-center pl-3">
              <span class="text-gray-500 sm:text-sm">$</span>
            </div>
            <input
              :id="`storeproduct-${storeProduct.id}__price`"
              :name="`storeproduct-${storeProduct.id}__price`"
              v-model="storeProduct.price"
              type="number"
              min="0"
              step="0.01"
              placeholder="0.00"
              aria-describedby="price-currency"
              class="block w-full rounded-md border-0 py-1.5 pl-7 text-gray-900 ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-indigo-600 sm:text-sm sm:leading-6"
            />
          </div>
          <div class="flex flex-row items-center justify-center">
            <input
              :id="`storeproduct-${storeProduct.id}__remove`"
              :name="`storeproduct-${storeProduct.id}__remove`"
              type="checkbox"
              v-model="storeProduct.shouldRemove"
              class="h-4 w-4 rounded border-gray-300 text-indigo-600 focus:ring-indigo-600"
            />
          </div>
        </div>
        <button
          v-if="!hasAllStores"
          type="button"
          class="rounded-md bg-white px-3 py-2 text-sm font-semibold text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 hover:ring-gray-400"
          @click="handleAddStore"
        >
          Assign a Store
        </button>
      </div>
    </div>
    <div class="flex flex-shrink-0 justify-end p-4 sm:p-6 border-t border-gray-200 space-x-2">
      <button
        type="button"
        class="rounded-md bg-red-600 px-3 py-2 text-sm font-semibold text-white shadow-sm ring-1 ring-inset ring-gray-300 hover:ring-gray-400"
        @click="handleProductDelete"
      >
        Delete
      </button>
      <button
        type="button"
        class="rounded-md bg-white px-3 py-2 text-sm font-semibold text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 hover:ring-gray-400"
        @click="handleProductCancel"
      >
        Cancel
      </button>
      <button
        type="submit"
        class="rounded-md bg-indigo-600 px-3 py-2 text-sm font-semibold text-white shadow-sm hover:bg-indigo-500 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-indigo-500"
        @click="handleProductSave"
      >
        Save
      </button>
    </div>
  </div>
</template>
