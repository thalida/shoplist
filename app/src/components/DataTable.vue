<script setup lang="ts">
import { computed, type PropType } from 'vue';
import { ChevronDownIcon, ListFilterIcon } from 'lucide-vue-next';
import { Popover, PopoverButton, PopoverPanel } from '@headlessui/vue'
import type { IPageInfo, IFilterBy, IOrderBy } from '@/types/graphql';
import { keyBy } from 'lodash';

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
  filterBy: {
    type: Object as PropType<IFilterBy>,
    required: false,
    default: () => ({}),
  },
  orderBy: {
    type: Array as PropType<IOrderBy[]>,
    required: false,
    default: () => ([]),
  },
})

const emit = defineEmits<{
  (e: 'nextPage', pageInfo: IPageInfo): void
  (e: 'prevPage', pageInfo: IPageInfo): void
  (e: 'updateOrderBy', header: IDataTableHeader): void
}>()

const numHeaders = computed(() => props.headers.length)
const numItems = computed(() => props.items.length)
const headerItemWidth = computed(() => {
  return `${100 / numHeaders.value}%`
})
const orderByField = computed(() => {
  return keyBy(props.orderBy, 'field')
})
</script>

<template>
  <div>
    <table class="min-w-full border-separate border-spacing-0">
      <thead>
        <tr>
          <th
            v-for="header in headers" :key="header.key"
            scope="col"
            class="sticky top-0 z-10 border-b border-gray-300 bg-white bg-opacity-75 px-3 py-3.5 text-left text-sm font-semibold text-gray-900 backdrop-blur backdrop-filter"
            :style= "{ width: headerItemWidth }"
          >
            <div class="flex flex-row justify-between items-center space-x-4">
              <button class="group inline-flex space-x-2" @click="emit('updateOrderBy', header)">
                <div>
                  <slot :name="`header-${header.key}:label`" :header="header">
                    {{ header.label }}
                  </slot>
                </div>
                <span
                  v-if="header.isSortable"
                  class="flex-none rounded text-gray-400 group-hover:visible group-focus:visible"
                  :class="{
                    invisible: typeof orderByField[header.key] === 'undefined' || orderByField[header.key]?.value === null,
                    'rotate-0': orderByField[header.key]?.value === true,
                    'rotate-180': orderByField[header.key]?.value === false,
                  }"
                >
                  <ChevronDownIcon class="h-5 w-5" aria-hidden="true" />
                </span>
              </button>
              <Popover v-if="header.isFilterable" class="relative">
                <PopoverButton>
                  <ListFilterIcon
                    class="h-5 w-5"
                    :class="{
                      'bg-red': typeof filterBy[header.key] !== 'undefined' && filterBy[header.key] !== null,
                    }"
                    aria-hidden="true"
                  />
                </PopoverButton>
                <PopoverPanel class="absolute right-4 z-10 bg-white border border-solid border-gray-200 p-4 -mx-4 rounded-md" :focus="true">
                  <div class="">
                    <slot :name="`header-${header.key}:filter`" :header="header">
                      filter
                    </slot>
                  </div>
                </PopoverPanel>
              </Popover>
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
    <nav v-if="pageInfo" class="flex items-center justify-between border-t border-gray-200 bg-white px-4 py-3" aria-label="Pagination">
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
  </div>
</template>
