<script setup lang="ts">
import { computed, ref, type PropType } from 'vue';
import { ChevronDownIcon, ListFilterIcon, XIcon, PlusIcon, MinusIcon } from 'lucide-vue-next';
import { Popover, PopoverButton, PopoverPanel } from '@headlessui/vue'
import { Dialog, DialogTitle, DialogPanel, TransitionChild, TransitionRoot } from '@headlessui/vue'
import { Disclosure, DisclosureButton, DisclosurePanel } from '@headlessui/vue'
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
const isFilterPanelOpen = ref(false)
</script>

<template>
  <div class="relative overflow-auto">
    <table class="min-w-full border-separate border-spacing-0">
      <thead>
        <tr>
          <th
            v-for="header in headers" :key="header.key"
            scope="col"
            class="border-b border-gray-300 bg-white px-3 py-3.5 text-left text-sm font-semibold text-gray-900"
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
                  class="flex-none rounded text-gray-400 group-hover:visible group-focus:visible"
                  :class="{
                    invisible: typeof orderByField[header.key] === 'undefined' || orderByField[header.key]?.value === null,
                    'rotate-0': orderByField[header.key]?.value === true,
                    'rotate-180': orderByField[header.key]?.value === false,
                  }"
                >
                  <ChevronDownIcon class="h-5 w-5" aria-hidden="true" />
                </span>
              </component>
              <button v-if="header.isFilterable" @click="isFilterPanelOpen = true">
                <ListFilterIcon
                  class="h-4 w-4"
                  :class="{
                    'bg-red': typeof filterBy[header.key] !== 'undefined' && filterBy[header.key] !== null,
                  }"
                  aria-hidden="true"
                />
              </button>
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

    <TransitionRoot as="template" :show="isFilterPanelOpen">
      <Dialog as="div" class="relative z-40" @close="isFilterPanelOpen = false">
        <TransitionChild as="template" enter="transition-opacity ease-linear duration-300" enter-from="opacity-0" enter-to="opacity-100" leave="transition-opacity ease-linear duration-300" leave-from="opacity-100" leave-to="opacity-0">
          <div class="fixed inset-0 bg-black bg-opacity-25" />
        </TransitionChild>

        <div class="fixed inset-0 z-40 flex">
          <TransitionChild as="template" enter="transition ease-in-out duration-300 transform" enter-from="translate-x-full" enter-to="translate-x-0" leave="transition ease-in-out duration-300 transform" leave-from="translate-x-0" leave-to="translate-x-full">
            <DialogPanel class="relative ml-auto flex h-full w-full max-w-xs flex-col overflow-y-auto bg-white pb-12 shadow-xl">
              <div class="sticky top-0 flex items-center justify-between p-4 bg-white bg-opacity-50 backdrop-blur-sm">
                <h2 class="text-lg font-medium text-gray-900">Filters</h2>
                <button type="button" class="-mr-2 flex h-10 w-10 items-center justify-center rounded-md bg-white p-2 text-gray-400" @click="isFilterPanelOpen = false">
                  <span class="sr-only">Close menu</span>
                  <XIcon class="h-6 w-6" aria-hidden="true" />
                </button>
              </div>

              <!-- Filters -->
              <form class="mt-4">
                <template v-for="header in headers" :key="header.key">
                  <Disclosure as="div" v-if="header.isFilterable" class="px-4 py-6" v-slot="{ open }">
                    <h3 class="-mx-2 -my-3 flow-root">
                      <DisclosureButton class="flex w-full items-center justify-between bg-white px-2 py-3 text-gray-400 hover:text-gray-500">
                        <span class="font-medium text-gray-900">{{ header.label }}</span>
                        <span class="ml-6 flex items-center">
                          <PlusIcon v-if="!open" class="h-5 w-5" aria-hidden="true" />
                          <MinusIcon v-else class="h-5 w-5" aria-hidden="true" />
                        </span>
                      </DisclosureButton>
                    </h3>
                    <DisclosurePanel class="pt-6">
                      <slot :name="`filter-panel-${header.key}`" :header="header"></slot>
                    </DisclosurePanel>
                  </Disclosure>
                </template>
              </form>
            </DialogPanel>
          </TransitionChild>
        </div>
      </Dialog>
    </TransitionRoot>
  </div>
</template>
