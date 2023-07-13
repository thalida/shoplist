<script setup lang="ts">
import { computed, onMounted } from 'vue';
import { XCircleIcon, ArrowUpWideNarrow } from 'lucide-vue-next';
import AppMain from '@/components/AppMain.vue';
import { useShopStore } from '@/stores/shop';
import DataTable, { type IDataTableHeader } from '@/components/DataTable.vue';

const shopStore = useShopStore();
const products = computed(() => shopStore.productsPageItems);
const isLoading = computed(() => shopStore.productsIsLoading);
const apiErrors = computed(() => shopStore.productsAPIErrors);
const pageInfo = computed(() => shopStore.productsPageInfo);
const orderBy = computed(() => shopStore.productsOrderBy);
const filterBy = computed(() => shopStore.productsFilterBy);

const headers: IDataTableHeader[] = [
  { label: "Name", key: "name", isSortable: true, isFilterable: true },
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
    name_Icontains: filterBy.value.name,
    category: filterBy.value.category,
    stores: filterBy.value.stores,
    lists: filterBy.value.lists,
  });
}

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
  loadData({
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
    Products View

    <div class="sm:flex sm:items-center">
      <div class="sm:flex-auto">
        <h1 class="text-base font-semibold leading-6 text-gray-900">Users</h1>
        <p class="mt-2 text-sm text-gray-700">A list of all the users in your account including their name, title, email and role.</p>
      </div>
      <div class="mt-4 sm:ml-16 sm:mt-0 sm:flex-none">
        <button type="button" class="block rounded-md bg-indigo-600 px-3 py-2 text-center text-sm font-semibold text-white shadow-sm hover:bg-indigo-500 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-indigo-600">Add user</button>
      </div>
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
      @nextPage="handleNextPage"
      @prevPage="handlePrevPage"
      @updateOrderBy="handleUpdateOrderBy"
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
      <template #filter-panel-name>
        <div>
          <label for="email" class="block text-sm font-medium leading-6 text-gray-900">Search candidates</label>
          <div class="mt-2 flex rounded-md shadow-sm">
            <div class="relative flex flex-grow items-stretch focus-within:z-10">
              <div class="pointer-events-none absolute inset-y-0 left-0 flex items-center pl-3">
                <UsersIcon class="h-5 w-5 text-gray-400" aria-hidden="true" />
              </div>
              <input type="email" name="email" id="email" class="block w-full rounded-none rounded-l-md border-0 py-1.5 pl-10 text-gray-900 ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-indigo-600 sm:text-sm sm:leading-6" placeholder="John Smith" />
            </div>
            <button type="button" class="relative -ml-px inline-flex items-center gap-x-1.5 rounded-r-md px-3 py-2 text-sm font-semibold text-gray-900 ring-1 ring-inset ring-gray-300 hover:bg-gray-50">
              <ArrowUpWideNarrow class="-ml-0.5 h-5 w-5 text-gray-400" aria-hidden="true" />
              Sort
            </button>
          </div>
        </div>
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
