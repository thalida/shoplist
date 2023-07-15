<script setup lang="ts">
import { computed, onMounted, ref, watch } from 'vue';
import { XCircleIcon, PlusIcon, ChevronsUpDownIcon, CheckIcon } from 'lucide-vue-next';
import { debounce } from 'lodash';
  import {
    Combobox,
    ComboboxButton,
    ComboboxInput,
    ComboboxOptions,
    ComboboxOption,
  } from '@headlessui/vue'
import AppMain from '@/components/AppMain.vue';
import { useShopStore } from '@/stores/shop';
import DataTable, { type IDataTableHeader } from '@/components/DataTable.vue';
import ColorBadge from '@/components/ColorBadge.vue';

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
{ label: "Category", key: "categories", isSortable: false, isFilterable: true },
{ label: "List", key: "lists", isSortable: false, isFilterable: true },
{ label: "Store", key: "stores", isSortable: false, isFilterable: true },
];
const pageSize = 3;

const filterCategoriesQuery = ref('')
const filterCategoriesSelected = ref([]);
const filteredCategories = computed(() =>
  filterCategoriesQuery.value === ''
    ? shopStore.productCategoryOrder
    : shopStore.productCategoryOrder.filter((uid) => {
        return shopStore.productCategories[uid].name
          .toLowerCase()
          .includes(filterCategoriesQuery.value.toLowerCase())
      })
)
watch(() => filterCategoriesSelected.value, () => {
  shopStore.setProductsFilterBy({
    ...filterBy.value,
    categories: filterCategoriesSelected.value,
  });
  loadData({
    first: pageSize,
  });
});

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
  await shopStore.getProductCategories();
  loadData({
    first: pageSize,
  })
});

function boldSearchQuery(query: string | null, text: string) {
  if (!query) {
    return text;
  }

  const regex = new RegExp(query, 'gi');
  return text.replace(regex, (match) => `<b>${match}</b>`);
}
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
      :showSearch="true"
      :searchQuery="searchQuery"
      :searchPlaceholder="'Search by product name'"
      @nextPage="handleNextPage"
      @prevPage="handlePrevPage"
      @updateOrderBy="handleUpdateOrderBy"
      @updateSearchQuery="handleUpdateSearchQuery"
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
          v-if="filterBy.categories?.length > 0"
          class="inline-flex items-center rounded-full bg-blue-100 px-1.5 py-0.5 text-xs font-medium text-blue-700"
        >
          {{ filterBy.categories?.length }}
        </span>
      </template>
      <template #filter-panel-categories>
        <div class="py-4">
          <div class="px-4">
            <Combobox as="template" v-model="filterCategoriesSelected" multiple :nullable="true">
              <div class="relative">
                <div class="relative">
                  <ComboboxInput
                    class="w-full rounded-md border-0 bg-white py-1.5 pl-3 pr-10 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 focus:ring-2 focus:ring-inset focus:ring-indigo-600 sm:text-sm sm:leading-6"
                    @change="filterCategoriesQuery = $event.target.value"
                    :displayValue="() => filterCategoriesQuery"
                    :placeholder="'Search categories'"
                  />
                  <ComboboxButton class="absolute inset-y-0 right-0 flex items-center rounded-r-md px-2 focus:outline-none">
                    <ChevronsUpDownIcon class="h-5 w-5 text-gray-400" aria-hidden="true" />
                  </ComboboxButton>
                </div>

                <ComboboxOptions v-if="filteredCategories.length > 0" class="absolute z-10 mt-1 max-h-60 w-full overflow-auto rounded-md bg-white py-1 text-base shadow-lg ring-1 ring-black ring-opacity-5 focus:outline-none sm:text-sm">
                  <ComboboxOption
                    as="template"
                    v-for="categoryUid in filteredCategories"
                    :key="categoryUid"
                    :value="categoryUid"
                    v-slot="{ active, selected }"
                  >
                    <li :class="['relative cursor-default select-none py-2 pl-3 pr-9', active ? 'bg-indigo-600 text-white' : 'text-gray-900']">
                      <span
                        :class="['block truncate']"
                        v-html="boldSearchQuery(filterCategoriesQuery, shopStore.productCategories[categoryUid].name)"
                      />

                      <span v-if="selected" :class="['absolute inset-y-0 right-0 flex items-center pr-4', active ? 'text-white' : 'text-indigo-600']">
                        <CheckIcon class="h-5 w-5" aria-hidden="true" />
                      </span>
                    </li>
                  </ComboboxOption>
                </ComboboxOptions>
              </div>
            </Combobox>
          </div>
          <div v-if="filterCategoriesSelected.length > 0" class="flex flex-row flex-wrap gap-1 max-h-40 mt-4 px-4 overflow-auto">
            <ColorBadge
              v-for="categoryUid in filterCategoriesSelected" :key="categoryUid"
              :label="shopStore.productCategories[categoryUid].name"
              :color="shopStore.productCategories[categoryUid].color"
              :showRemoveButton="true"
              @remove="() => filterCategoriesSelected = filterCategoriesSelected.filter((uid) => uid !== categoryUid)"
            />
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
