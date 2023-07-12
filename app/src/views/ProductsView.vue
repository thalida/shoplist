<script setup lang="ts">
import { computed, onMounted } from 'vue';
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
  const orderByStr = shopStore.formatOrderByArgs(orderBy.value);

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
  shopStore.toggleOrderByField(orderBy.value, header.key);
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

    <div>
      {{ apiErrors }}
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
    />
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
