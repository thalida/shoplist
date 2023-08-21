<script setup lang="ts">
import { computed, ref, watch, watchEffect, type PropType} from 'vue';
import {
  Combobox,
  ComboboxButton,
  ComboboxInput,
  ComboboxOptions,
  ComboboxOption,
} from '@headlessui/vue';
import { ChevronsUpDownIcon, CheckIcon } from 'lucide-vue-next';


const props = defineProps({
  items: {
    type: Array as PropType<Record<string, any>[]>,
    required: true,
  },
  selected: {
    type: Array as PropType<string[]>,
    required: true,
  },
  idKey: {
    type: String,
    required: false,
    default: 'id',
  },
  labelKey: {
    type: String,
    required: false,
    default: 'name',
  },
  valueKey: {
    type: String,
    required: false,
    default: 'id',
  },
  inputPlaceholder: {
    type: String,
    required: false,
    default: 'Search items',
  },
});

const emit = defineEmits<{
  (e: 'update:selected', value: any): void;
}>();

const query = ref('')
const localSelected = ref<string[]>(props.selected)
const filteredItems = computed(() =>
  query.value === ''
    ? props.items
    : props.items.filter((item) => {
        return item[props.labelKey]
          .toLowerCase()
          .includes(query.value.toLowerCase())
      })
)

function boldSearchQuery(query: string | null, text: string) {
  if (!query) {
    return text;
  }

  const regex = new RegExp(query, 'gi');
  return text.replace(regex, (match) => `<b>${match}</b>`);
}

function removeItem(item: string) {
  const index = localSelected.value.indexOf(item)
  if (index > -1) {
    localSelected.value.splice(index, 1)
  }

  emit('update:selected', localSelected.value)
}

watchEffect(() => {
  localSelected.value = props.selected
})

defineExpose({
  removeItem,
})
</script>

<template>
  <div>
    <Combobox
      as="template"
      v-model="localSelected"
      multiple
      :nullable="true"
      @update:model-value="emit('update:selected', $event)"
    >
      <div class="relative">
        <div class="relative">
          <ComboboxInput
            class="w-full rounded-md border-0 bg-white py-1.5 pl-3 pr-10 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 focus:ring-2 focus:ring-inset focus:ring-indigo-600 sm:text-sm sm:leading-6"
            @change="query = $event.target.value"
            :displayValue="() => query"
            :placeholder="inputPlaceholder"
          />
          <ComboboxButton class="absolute inset-y-0 right-0 flex items-center rounded-r-md px-2 focus:outline-none">
            <ChevronsUpDownIcon class="h-5 w-5 text-gray-400" aria-hidden="true" />
          </ComboboxButton>
        </div>

        <ComboboxOptions v-if="filteredItems.length > 0" class="absolute z-10 mt-1 max-h-60 w-full overflow-auto rounded-md bg-white py-1 text-base shadow-lg ring-1 ring-black ring-opacity-5 focus:outline-none sm:text-sm">
          <ComboboxOption
            as="template"
            v-for="item in filteredItems"
            :key="item[idKey]"
            :value="item[valueKey]"
            v-slot="{ active, selected }"
          >
            <li :class="['relative cursor-default select-none py-2 pl-3 pr-9', active ? 'bg-indigo-600 text-white' : 'text-gray-900']">
              <span
                :class="['block truncate']"
                v-html="boldSearchQuery(query, item[labelKey])"
              />

              <span v-if="selected" :class="['absolute inset-y-0 right-0 flex items-center pr-4', active ? 'text-white' : 'text-indigo-600']">
                <CheckIcon class="h-5 w-5" aria-hidden="true" />
              </span>
            </li>
          </ComboboxOption>
        </ComboboxOptions>
      </div>
    </Combobox>
    <div v-if="selected.length > 0" class="flex flex-row flex-wrap gap-1 max-h-40 mt-4 overflow-auto">
      <slot name="selected" :selected="selected" />
    </div>
  </div>
</template>

<style scoped>

</style>
