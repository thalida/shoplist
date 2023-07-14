<script setup lang="ts">
import { computed, onMounted, ref } from 'vue';
import { XCircleIcon, PlusIcon } from 'lucide-vue-next';
import AppMain from '@/components/AppMain.vue';
import { useShopStore } from '@/stores/shop';
import DataTable, { type IDataTableHeader } from '@/components/DataTable.vue';
import { debounce } from 'lodash';

const shopStore = useShopStore();
const products = computed(() => shopStore.productsPageItems);
const isLoading = computed(() => shopStore.productsIsLoading);
const apiErrors = computed(() => shopStore.productsAPIErrors);
const pageInfo = computed(() => shopStore.productsPageInfo);
const orderBy = computed(() => shopStore.productsOrderBy);
const filterBy = computed(() => shopStore.productsFilterBy);
const searchQuery = ref('');

const headers: IDataTableHeader[] = [
{ label: "Name", key: "name", isSortable: true, isFilterable: false },
{ label: "Category", key: "category", isSortable: true, isFilterable: true },
{ label: "Lists", key: "lists", isSortable: false, isFilterable: true },
{ label: "Stores", key: "stores", isSortable: false, isFilterable: true },
];
const pageSize = 50;

async function loadData({ first, last, after, before }: { first?: number, last?: number, after?: string, before?: string }) {
  const orderByStr = shopStore.formatOrderByArgs(orderBy.value, { category: 'category__name' });

  shopStore.getProducts({
    first,
    last,
    after,
    before,
    orderBy: orderByStr,
    ...filterBy.value,
  });
}

const debouncedLoadData = debounce(loadData, 300);

function handleNextPage(){
  loadData({
    first: pageSize,
    after: pageInfo.value.endCursor || undefined,
  });
}

function handlePrevPage(){
  loadData({
    last: pageSize,
    before: pageInfo.value.startCursor || undefined,
  });
}

function handleUpdateOrderBy(header: IDataTableHeader) {
  const newOrderBy = shopStore.toggleOrderByField(orderBy.value, header.key);
  shopStore.setProductsOrderBy(newOrderBy);
  debouncedLoadData({
    first: pageSize,
  });
}

function handleUpdateSearchQuery(newSearchQuery: string) {
  searchQuery.value = newSearchQuery;
  shopStore.setProductsFilterBy({
    ...filterBy.value,
    name_Icontains: searchQuery.value,
  });
  debouncedLoadData({
    first: pageSize,
  });
}

onMounted(async () => {
  loadData({
    first: pageSize,
  })
});
</script>

<template>
  <AppMain>
    <div class="flex flex-row items-center justify-between">
      <h1 class="text-base font-semibold leading-6 text-gray-900">All Products</h1>

      <button
        type="button"
        class="flex flex-row space-x-2 items-center justify-center rounded-md bg-indigo-600 px-3 py-2 text-center text-sm font-semibold text-white shadow-sm hover:bg-indigo-500 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-indigo-600"
      >
        <PlusIcon
          class="h-4 w-4"
          aria-hidden="true" />
        <span>Add Product</span>
      </button>
    </div>

    <div v-if="apiErrors" class="rounded-md bg-red-50 p-4">
      <div class="flex">
        <div class="flex-shrink-0">
          <XCircleIcon class="h-5 w-5 text-red-400" aria-hidden="true" />
        </div>
        <div class="ml-3">
          <h3 class="text-sm font-medium text-red-800">There was an error loading products</h3>
          <div class="mt-2 text-sm text-red-700">
            <ul role="list" class="list-disc space-y-1 pl-5">
              <li v-for="(error, errorKey) in apiErrors" :key="errorKey">
                {{ errorKey }}
                <ul>
                  <li v-for="(errorItem, errorItemKey) in error" :key="errorItemKey">
                    {{ errorItem.message }}
                  </li>
                </ul>
              </li>
            </ul>
          </div>
        </div>
      </div>
    </div>

    <DataTable
      :isLoading="isLoading"
      :headers="headers"
      :items="products"
      :pageInfo="pageInfo"
      :orderBy="orderBy"
      :filterBy="filterBy"
      :showFilterButton="true"
      :showSelectedFilters="true"
      :showSearch="true"
      :searchQuery="searchQuery"
      :searchPlaceholder="'Search product by name'"
      @nextPage="handleNextPage"
      @prevPage="handlePrevPage"
      @updateOrderBy="handleUpdateOrderBy"
      @updateSearchQuery="handleUpdateSearchQuery"
    >
      <template #item-category="{ item }">
        <div v-if="item.category">
          <span
            class="inline-flex items-center rounded-md ring-1 ring-inset px-2 py-1 text-xs font-medium "
            :class="{
              'bg-white text-gray-600 ring-gray-300': item.category.color === 'white',
              'bg-gray-50 text-gray-600 ring-gray-500/10': item.category.color === 'gray',
              'bg-orange-800 text-orange-200 ring-orange-900': item.category.color === 'brown',
              'bg-slate-900 text-white ring-black/10': item.category.color === 'black',
              'bg-red-50 text-red-700 ring-red-600/10': item.category.color === 'red',
              'bg-yellow-50 text-yellow-800 ring-yellow-600/20': item.category.color === 'yellow',
              'bg-green-50 text-green-700 ring-green-600/20': item.category.color === 'green',
              'bg-blue-50 text-blue-700 ring-blue-700/10': item.category.color === 'blue',
              'bg-purple-50 text-purple-700 ring-purple-700/10': item.category.color === 'purple',
              'bg-pink-50 text-pink-700 ring-pink-700/10': item.category.color === 'pink',
            }"
          >
            {{ item.category.name }}
          </span>
        </div>
      </template>
      <template #filter-panel-category>
        Category
      </template>
    </DataTable>
  </AppMain>
</template>

<style scoped>
.filter-menu {
  position: absolute;
  background-color: white;
  border: 1px solid #ccc;
  border-radius: 5px;
  padding: 5px;
}
</style>
