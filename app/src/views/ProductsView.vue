<script setup lang="ts">
import { computed, onMounted, ref, type Ref } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import { XCircleIcon, PlusIcon } from 'lucide-vue-next';
import { debounce } from 'lodash';
import { TransitionRoot, TransitionChild } from '@headlessui/vue';
import { PRODUCTS_ROUTE, PRODUCT_DETAIL_ROUTE } from '@/router';
import { Dialog, DialogPanel } from '@headlessui/vue';
import AppMain from '@/components/AppMain.vue';
import DataTable, { type IDataTableHeader } from '@/components/DataTable.vue';
import ColorBadge from '@/components/ColorBadge.vue';
import ComboboxFilter from '@/components/ComboboxFilter.vue';
import { formatOrderByArgs, toggleOrderByField } from '@/utils/api';
import { useProductStore } from '@/stores/product';
import { useListStore } from '@/stores/list';
import { useStoreStore } from '@/stores/store';

const router = useRouter();
const route = useRoute();
const listStore = useListStore();
const storeStore = useStoreStore();
const productStore = useProductStore();

const isDetailRoute = computed(() => route.matched.some((m) => m.name === PRODUCT_DETAIL_ROUTE));

const categoriesComboxFilter: Ref<InstanceType<typeof ComboboxFilter> | null> = ref(null);
const listsComboxFilter: Ref<InstanceType<typeof ComboboxFilter> | null> = ref(null);

const headers: IDataTableHeader[] = [
  { label: "Name", key: "name", isSortable: true, isFilterable: false },
  { label: "Category", key: "categories", isSortable: false, isFilterable: true },
  { label: "List", key: "lists", isSortable: false, isFilterable: true },
  { label: "Store", key: "stores", isSortable: false, isFilterable: true },
];
const pageSize = 3;
const searchQuery = ref('');

async function loadData({ first, last, after, before }: { first?: number, last?: number, after?: string, before?: string }) {
  const orderByStr = formatOrderByArgs(productStore.orderBy, { category: 'category__name' });

  productStore.fetch({
    first,
    last,
    after,
    before,
    orderBy: orderByStr,
    ...productStore.filterBy,
  });
}

const debouncedLoadData = debounce(loadData, 300);

function handleClickRowItem(item: Record<string, any>) {
  router.push({
    name: PRODUCT_DETAIL_ROUTE,
    params: {
      productId: item.uid,
    },
  });
}

function handleNextPage(){
  loadData({
    first: pageSize,
    after: productStore.pageInfo.endCursor || undefined,
  });
}

function handlePrevPage(){
  loadData({
    last: pageSize,
    before: productStore.pageInfo.startCursor || undefined,
  });
}

function handleUpdateOrderBy(header: IDataTableHeader) {
  const newOrderBy = toggleOrderByField(productStore.orderBy, header.key);
  productStore.setOrderBy(newOrderBy);
  debouncedLoadData({
    first: pageSize,
  });
}

function handleUpdateSearchQuery(newSearchQuery: string) {
  searchQuery.value = newSearchQuery;
  productStore.setFilterBy({
    ...productStore.filterBy,
    name_Icontains: searchQuery.value,
  });
  debouncedLoadData({
    first: pageSize,
  });
}

function handleDetailPanelClose() {
  router.push({
    name: PRODUCTS_ROUTE,
    params: {
      productId: null,
    },
  });
}

// function handleSelectedCategoriesChanged(field, selectedItems: string[]) {
//   productStore.setFilterBy({
//     ...productStore.filterBy,
//     categories: selectedItems,
//   });
//   debouncedLoadData({
//     first: pageSize,
//   });
// }

// function handleSelectedListsChanged(field, selectedItems: string[]) {
//   productStore.setFilterBy({
//     ...productStore.filterBy,
//     lists: selectedItems,
//   });
//   debouncedLoadData({
//     first: pageSize,
//   });
// }

function handleFiltersChanged(field: string, selectedItems: string[]) {
  productStore.setFilterBy({
    ...productStore.filterBy,
    [field]: selectedItems,
  });
  debouncedLoadData({
    first: pageSize,
  });
}

onMounted(async () => {
  await Promise.all([
    storeStore.fetch(),
    listStore.fetch(),
    productStore.getCategories(),
  ]);
  loadData({
    first: pageSize,
  })
});
</script>

<template>
  <AppMain>
    <div>
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

      <div v-if="productStore.errors" class="rounded-md bg-red-50 p-4">
        <div class="flex">
          <div class="flex-shrink-0">
            <XCircleIcon class="h-5 w-5 text-red-400" aria-hidden="true" />
          </div>
          <div class="ml-3">
            <h3 class="text-sm font-medium text-red-800">There was an error loading products</h3>
            <div class="mt-2 text-sm text-red-700">
              <ul role="list" class="list-disc space-y-1 pl-5">
                <li v-for="(error, errorKey) in productStore.errors" :key="errorKey">
                  <ul>
                    <li v-for="(errorItem, errorItemKey) in error" :key="errorItemKey">
                      {{ errorItem }}
                    </li>
                  </ul>
                </li>
              </ul>
            </div>
          </div>
        </div>
      </div>

      <DataTable
        :isLoading="productStore.isLoading"
        :headers="headers"
        :items="productStore.pageItems"
        :pageInfo="productStore.pageInfo"
        :orderBy="productStore.orderBy"
        :filterBy="productStore.filterBy"
        :showSearch="true"
        :searchQuery="searchQuery"
        :searchPlaceholder="'Search by product name'"
        @nextPage="handleNextPage"
        @prevPage="handlePrevPage"
        @updateOrderBy="handleUpdateOrderBy"
        @updateSearchQuery="handleUpdateSearchQuery"
        @clickRowItem="handleClickRowItem"
      >
        <template #item-categories="{ item }">
          <div class="flex flex-row flex-wrap gap-1">
            <ColorBadge
              v-for="category in item.categories"
              :key="category.uid"
              :label="category.name"
              :color="category.color"
            />
          </div>
        </template>
        <template #filter-status-categories>
          <span
            v-if="productStore.filterBy.categories?.length > 0"
            class="inline-flex items-center rounded-full bg-blue-100 px-1.5 py-0.5 text-xs font-medium text-blue-700"
          >
            {{ productStore.filterBy.categories?.length }}
          </span>
        </template>
        <template #filter-panel-categories>
          <ComboboxFilter
            ref="categoriesComboxFilter"
            :items="productStore.categories"
            :selected="productStore.filterBy.categories"
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
        </template>
        <template #filter-panel-lists>
          <ComboboxFilter
            ref="listsComboxFilter"
            :items="Object.values(listStore.collection)"
            :selected="productStore.filterBy.lists"
            labelKey="name"
            valueKey="uid"
            idKey="uid"
            inputPlaceholder="Search lists"
            @update:selected="(items) => handleFiltersChanged('lists', items)"
          >
            <template #selected="{ selected }">
              <div v-for="itemId in selected" :key="itemId">
                {{ listStore.collection[itemId].name }}
              </div>
            </template>
          </ComboboxFilter>
        </template>
        <template #filter-panel-stores>
          <ComboboxFilter
            ref="listsComboxFilter"
            :items="Object.values(storeStore.collection)"
            :selected="productStore.filterBy.stores"
            labelKey="name"
            valueKey="uid"
            idKey="uid"
            inputPlaceholder="Search stores"
            @update:selected="(items) => handleFiltersChanged('stores', items)"
          >
            <template #selected="{ selected }">
              <div v-for="itemId in selected" :key="itemId">
                {{ storeStore.collection[itemId].name }}
              </div>
            </template>
          </ComboboxFilter>
        </template>
      </DataTable>
    </div>
    <TransitionRoot as="template" :show="isDetailRoute">
      <Dialog as="div" class="relative z-40" @close="handleDetailPanelClose">
        <TransitionChild as="template" enter="transition-opacity ease-linear duration-300" enter-from="opacity-0" enter-to="opacity-100" leave="transition-opacity ease-linear duration-300" leave-from="opacity-100" leave-to="opacity-0">
          <div class="fixed inset-0 bg-black bg-opacity-25" />
        </TransitionChild>

        <div class="fixed inset-0 z-40 flex">
          <TransitionChild as="template" enter="transition ease-in-out duration-300 transform" enter-from="translate-x-full" enter-to="translate-x-0" leave="transition ease-in-out duration-300 transform" leave-from="translate-x-0" leave-to="translate-x-full">
            <DialogPanel class="relative pointer-events-auto ml-auto flex h-full w-screen max-w-2xl flex-col overflow-y-auto bg-white shadow-xl">
              <RouterView />
            </DialogPanel>
          </TransitionChild>
        </div>
      </Dialog>
    </TransitionRoot>
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
