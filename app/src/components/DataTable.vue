<script setup lang="ts">
import { computed, type PropType } from 'vue';
import { ChevronsUpDownIcon, ChevronUpIcon, ChevronDownIcon, ChevronLeftIcon, ChevronRightIcon } from 'lucide-vue-next';
import { Popover, PopoverButton, PopoverPanel } from '@headlessui/vue'
import type { IPageInfo, IFilterBy, IOrderBy } from '@/types/api';
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
    default: null,
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
  (e: 'clickRowItem', item: Record<string, any>): void
}>()

const numHeaders = computed(() => props.headers.length)
const numItems = computed(() => props.items.length)
const headerItemWidth = computed(() => {
  return `${100 / numHeaders.value}%`
})
const orderByField = computed(() => {
  return keyBy(props.orderBy, 'field')
})

function handleSearchQueryChange(e: Event) {
  const target = e.target as HTMLInputElement;
  emit('updateSearchQuery', target.value);
}
</script>

<template>
  <div class="relative">
    <div class="flex flex-row flex-wrap-reverse sm:flex-wrap justify-between my-4 gap-4">
      <div class="flex flex-row items-center space-x-2 overflow-auto sm:overflow-visible">
        <template v-for="header in headers" :key="header.key">
          <Popover v-if="header.isFilterable" class="sm:relative inline-block text-left">
            <PopoverButton class="inline-flex w-full justify-center gap-x-1.5 rounded-md bg-white px-3 py-2 text-sm font-semibold text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 hover:bg-gray-50">
              {{ header.label }}
              <slot :name="`filter-status-${header.key}`" :header="header"></slot>
              <ChevronDownIcon class="ui-open:rotate-180 ui-open:transform -mr-1 h-5 w-5 text-gray-400" aria-hidden="true" />
            </PopoverButton>

            <transition enter-active-class="transition ease-out duration-100" enter-from-class="transform opacity-0 scale-95" enter-to-class="transform opacity-100 scale-100" leave-active-class="transition ease-in duration-75" leave-from-class="transform opacity-100 scale-100" leave-to-class="transform opacity-0 scale-95">
              <PopoverPanel class="absolute left-0 z-10 mt-2 w-56 max-h-80 origin-top-right rounded-md bg-white shadow-lg ring-1 ring-black ring-opacity-5 focus:outline-none">
                <slot :name="`filter-panel-${header.key}`" :header="header"></slot>
              </PopoverPanel>
            </transition>
          </Popover>
        </template>
      </div>
      <div v-if="showSearch" class="relative flex flex-row items-stretch focus-within:z-10 w-full sm:w-1/3 sm:min-w-60">
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
    <div
      class="overflow-auto border border-gray-300 rounded-t-lg"
      :class="[
        { 'rounded-b-lg': isLoading || numItems === 0 },
      ]">
      <table class="overflow-hidden min-w-full border-separate border-spacing-0">
        <thead class="bg-slate-100">
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
          <tr
            v-else
            v-for="(item, itemIdx) in items"
            :key="itemIdx"
            class="group cursor-pointer"
            tabindex="0"
            @click="emit('clickRowItem', item)"
            @keyup.enter="emit('clickRowItem', item)"
          >
            <td
              v-for="(header, headerIdx) in headers" :key="header.key"
              :class="[
                headerIdx === 0 ? 'whitespace-nowrap font-semibold' : '',
                itemIdx !== numItems - 1 ? 'border-b border-gray-200' : '',
                itemIdx % 2 === 0 ? 'bg-white' : 'bg-slate-50',
                'px-3 py-4 text-sm text-gray-500 group-hover:bg-slate-100'
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
    <nav v-if="pageInfo && numItems > 0" class="flex items-center justify-between rounded-b-lg border-x border-b border-gray-300 bg-white px-4 py-3" aria-label="Pagination">
      <p v-if="pageInfo.totalCount" class="text-sm text-gray-700">
        <span class="font-medium">{{ pageInfo.totalCount }}</span> result{{ pageInfo.totalCount > 1 ? 's' : '' }}
      </p>

      <span v-if="pageInfo.hasPreviousPage || pageInfo.hasNextPage" class="isolate inline-flex rounded-md shadow-sm">
        <button
          type="button"
          class="relative inline-flex items-center rounded-l-md bg-white px-2 py-2 text-gray-400 ring-1 ring-inset ring-gray-300 hover:bg-gray-50 focus:z-10 disabled:opacity-50"
          @click="emit('prevPage', pageInfo)"
          :disabled="!pageInfo.hasPreviousPage"
        >
          <span class="sr-only">Previous</span>
          <ChevronLeftIcon class="h-5 w-5" aria-hidden="true" />
        </button>
        <button
          type="button"
          class="relative -ml-px inline-flex items-center rounded-r-md bg-white px-2 py-2 text-gray-400 ring-1 ring-inset ring-gray-300 hover:bg-gray-50 focus:z-10 disabled:opacity-50"
          @click="emit('nextPage', pageInfo)"
          :disabled="!pageInfo.hasNextPage"
        >
          <span class="sr-only">Next</span>
          <ChevronRightIcon class="h-5 w-5" aria-hidden="true" />
        </button>
      </span>
    </nav>
  </div>
</template>
