<script setup lang="ts">
import { computed, ref, type PropType } from 'vue';
import { ChevronsUpDownIcon, ChevronUpIcon, ChevronDownIcon, ListFilterIcon, XIcon, PlusIcon, MinusIcon } from 'lucide-vue-next';
import { Dialog, DialogPanel, TransitionChild, TransitionRoot } from '@headlessui/vue'
import { Disclosure, DisclosureButton, DisclosurePanel } from '@headlessui/vue'
import type { IPageInfo, IFilterBy, IOrderBy } from '@/types/graphql';
import { keyBy } from 'lodash';
import { SearchIcon } from 'lucide-vue-next';

export interface IDataTableHeader {
  key: string,
  label: string,
  isSortable?: boolean,
  isFilterable?: boolean,
}

const props = defineProps({
  isLoading: {
    type: Boolean,
    required: false,
    default: false,
  },
  headers: {
    type: Array as PropType<IDataTableHeader[]>,
    required: true,
  },
  items: {
    type: Array as PropType<Record<string, any>[]>,
    required: true,
  },
  pageInfo: {
    type: Object as PropType<IPageInfo>,
    required: false,
  },
  orderBy: {
    type: Array as PropType<IOrderBy[]>,
    required: false,
    default: () => ([]),
  },
  filterBy: {
    type: Object as PropType<IFilterBy>,
    required: false,
    default: () => ({}),
  },
  showFilterButton: {
    type: Boolean,
    required: false,
    default: true,
  },
  filterButtonLabel: {
    type: String,
    required: false,
    default: 'Filter',
  },
  showSelectedFilters: {
    type: Boolean,
    required: false,
    default: true,
  },
  searchQuery: {
    type: String,
    required: false,
    default: '',
  },
  showSearch: {
    type: Boolean,
    required: false,
    default: true,
  },
  searchPlaceholder: {
    type: String,
    required: false,
    default: 'Search items',
  },
})

const emit = defineEmits<{
  (e: 'nextPage', pageInfo: IPageInfo): void
  (e: 'prevPage', pageInfo: IPageInfo): void
  (e: 'updateOrderBy', header: IDataTableHeader): void
  (e: 'updateSearchQuery', query: string): void
}>()

const numHeaders = computed(() => props.headers.length)
const numItems = computed(() => props.items.length)
const headerItemWidth = computed(() => {
  return `${100 / numHeaders.value}%`
})
const orderByField = computed(() => {
  return keyBy(props.orderBy, 'field')
})
const isFilterPanelOpen = ref(false)

function handleSearchQueryChange(e: Event) {
  const target = e.target as HTMLInputElement;
  emit('updateSearchQuery', target.value);
}
</script>

<template>
  <div class="relative">
    <div class="flex flex-row justify-between my-4">
      <div class="flex flex-row items-center space-x-2 lg:space-x-4">
        <button
          v-if="showFilterButton"
          @click="isFilterPanelOpen = true"
          type="button"
          class="flex flex-row space-x-2 items-center justify-center rounded-md bg-white px-3 py-2 text-center text-sm font-semibold text-indigo-600 border border-indigo-300 shadow-sm hover:bg-indigo-500 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-indigo-600"
        >
          <ListFilterIcon
            class="h-4 w-4"
            aria-hidden="true"
          />
          <span>{{ filterButtonLabel }}</span>
        </button>
        <div v-if="showSelectedFilters">
        </div>
      </div>
      <div v-if="showSearch" class="relative flex flex-row items-stretch focus-within:z-10 w-1/3 min-w-60">
        <div class="pointer-events-none absolute inset-y-0 left-0 flex items-center pl-3">
          <SearchIcon class="h-5 w-5 text-gray-400" aria-hidden="true" />
        </div>
        <input
          type="text"
          class="block w-full rounded-lg border-0 py-1.5 pl-10 text-gray-900 ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-indigo-600 sm:text-sm sm:leading-6"
          :placeholder="searchPlaceholder"
          :value="searchQuery"
          @input="handleSearchQueryChange"
        />
      </div>
    </div>
    <div class="overflow-auto border border-gray-300 rounded-t-lg">
      <table class="overflow-hidden min-w-full border-separate border-spacing-0">
        <thead class="bg-gray-50">
          <tr>
            <th
              v-for="header in headers" :key="header.key"
              scope="col"
              class="border-b border-gray-300 px-3 py-3.5 text-left text-sm font-semibold text-gray-900"
              :style= "{ width: headerItemWidth }"
            >
              <div class="flex flex-row justify-between items-center space-x-4">
                <component
                  :is="header.isSortable ? 'button' : 'div'"
                  @click="header.isSortable ? emit('updateOrderBy', header) : null"
                  class="group inline-flex space-x-2"
                >
                  <div>
                    <slot :name="`header-${header.key}:label`" :header="header">
                      {{ header.label }}
                    </slot>
                  </div>
                  <span
                    v-if="header.isSortable"
                    class="flex-none rounded text-gray-400"
                  >
                  <ChevronDownIcon v-if="orderByField[header.key]?.value === true" class="h-5 w-5" aria-hidden="true" />
                  <ChevronUpIcon v-else-if="orderByField[header.key]?.value === false" class="h-5 w-5" aria-hidden="true" />
                  <ChevronsUpDownIcon v-else class="h-5 w-5" aria-hidden="true" />
                  </span>
                </component>
              </div>
            </th>
          </tr>
        </thead>
        <tbody>
          <tr v-if="isLoading">
            <td class="px-3 py-4 text-sm text-gray-500 text-center" :colspan="headers.length + 1">
              <slot name="empty">
                Loading...
              </slot>
            </td>
          </tr>
          <tr v-else-if="numItems === 0">
            <td class="px-3 py-4 text-sm text-gray-500 text-center" :colspan="headers.length + 1">
              <slot name="empty">
                No items found.
              </slot>
            </td>
          </tr>
          <tr v-else v-for="(item, itemIdx) in items" :key="itemIdx">
            <td
              v-for="(header, headerIdx) in headers" :key="header.key"
              :class="[
                headerIdx === 0 ? 'whitespace-nowrap' : '',
                itemIdx !== numItems - 1 ? 'border-b border-gray-200' : '',
                itemIdx % 2 === 0 ? 'bg-white' : 'bg-slate-50',
                'px-3 py-4 text-sm text-gray-500'
              ]"
            >
              <slot :name="`item-${header.key}`" :item="item" :header="header">
                {{ item[header.key] }}
              </slot>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
    <nav v-if="pageInfo" class="flex items-center justify-between rounded-b-lg border-x border-b border-gray-300 bg-white px-4 py-3" aria-label="Pagination">
      <p v-if="pageInfo.totalCount" class="text-sm text-gray-700">
        <span class="font-medium">{{ pageInfo.totalCount }}</span> results
      </p>
      <div v-if="pageInfo.hasPreviousPage || pageInfo.hasNextPage" class="flex flex-1 justify-between sm:justify-end">
        <button
          @click="emit('prevPage', pageInfo)"
          :disabled="!pageInfo.hasPreviousPage"
          class="relative inline-flex items-center rounded-md bg-white px-3 py-2 text-sm font-semibold text-gray-900 ring-1 ring-inset ring-gray-300 hover:bg-gray-50 focus-visible:outline-offset-0 disabled:opacity-50">
          Previous
        </button>
        <button
          @click="emit('nextPage', pageInfo)"
          :disabled="!pageInfo.hasNextPage"
          class="relative ml-3 inline-flex items-center rounded-md bg-white px-3 py-2 text-sm font-semibold text-gray-900 ring-1 ring-inset ring-gray-300 hover:bg-gray-50 focus-visible:outline-offset-0 disabled:opacity-50">
          Next
        </button>
      </div>
    </nav>

    <TransitionRoot as="template" :show="isFilterPanelOpen">
      <Dialog as="div" class="relative z-40" @close="isFilterPanelOpen = false">
        <TransitionChild as="template" enter="transition-opacity ease-linear duration-300" enter-from="opacity-0" enter-to="opacity-100" leave="transition-opacity ease-linear duration-300" leave-from="opacity-100" leave-to="opacity-0">
          <div class="fixed inset-0 bg-black bg-opacity-25" />
        </TransitionChild>

        <div class="fixed inset-0 z-40 flex">
          <TransitionChild as="template" enter="transition ease-in-out duration-300 transform" enter-from="translate-x-full" enter-to="translate-x-0" leave="transition ease-in-out duration-300 transform" leave-from="translate-x-0" leave-to="translate-x-full">
            <DialogPanel class="relative ml-auto flex h-full w-full max-w-xs flex-col overflow-y-auto bg-white pb-12 shadow-xl space-y-4">
              <div class="sticky top-0 flex items-center justify-between p-4 bg-white bg-opacity-50 backdrop-blur-sm">
                <h2 class="text-lg font-medium text-gray-900">Filters</h2>
                <button type="button" class="-mr-2 flex h-10 w-10 items-center justify-center rounded-md bg-white p-2 text-gray-400" @click="isFilterPanelOpen = false">
                  <span class="sr-only">Close menu</span>
                  <XIcon class="h-6 w-6" aria-hidden="true" />
                </button>
              </div>

              <!-- Filters -->
              <form class="p-4">
                <template v-for="header in headers" :key="header.key">
                  <slot :name="`filter-panel-${header.key}`" :header="header"></slot>
                </template>
              </form>
            </DialogPanel>
          </TransitionChild>
        </div>
      </Dialog>
    </TransitionRoot>
  </div>
</template>
