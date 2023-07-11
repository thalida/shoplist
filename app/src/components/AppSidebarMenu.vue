<script setup lang="ts">
import { computed } from 'vue';
import {
  BuildingStorefrontIcon,
  QueueListIcon,
  Squares2X2Icon,
  PowerIcon,
} from '@heroicons/vue/24/outline'
import { useUserStore } from '@/stores/user';
import { getFullName } from '@/utils/user';
import AuthButton from '@/components/AuthButton.vue';
import UserAvatar from '@/components/UserAvatar.vue';

const userStore = useUserStore()
const myFullName = computed(() => {
  return userStore.me ? getFullName(userStore.me) : null
})

const isAuthenticated = computed(() => {
  return userStore.isAuthenticated;
});

const pinnedLists = [
  { id: 1, name: 'Grocery', href: '#', initial: 'H', current: false },
  { id: 2, name: 'Home Goods', href: '#', initial: 'T', current: false },
]

const recentLists = [
  { id: 1, name: 'Misc', href: '#', initial: 'H', current: false },
  { id: 2, name: 'Packing', href: '#', initial: 'T', current: false },
]

</script>

<template>
  <div class="flex grow flex-col gap-y-5 overflow-y-auto bg-gray-900 px-6">
    <div class="flex h-16 shrink-0 items-center">
      <img class="h-8 w-auto" src="https://tailwindui.com/img/logos/mark.svg?color=indigo&shade=500" alt="Your Company" />
    </div>
    <nav class="flex flex-1 flex-col">
      <ul role="list" class="flex flex-1 flex-col gap-y-7">
        <li class="space-y-3">
          <ul role="list" class="-mx-2 space-y-1">
            <li>
              <a href="#" :class="['text-gray-400 hover:text-white hover:bg-gray-800', 'group flex gap-x-3 rounded-md p-2 text-sm leading-6 font-semibold']">
                <QueueListIcon class="h-6 w-6 shrink-0" aria-hidden="true" />
                Lists
              </a>
              <div v-if="userStore.isAuthenticated" class="divide-y divide-gray-700 space-y-4 p-2">
                <div>
                  <div class="text-xs font-semibold leading-6 text-gray-300">Pinned</div>
                  <ul role="list" class="-mx-2 space-y-1">
                    <li v-for="team in pinnedLists" :key="team.name">
                      <a :href="team.href" :class="[team.current ? 'bg-gray-800 text-white' : 'text-gray-400 hover:text-white hover:bg-gray-800', 'group flex gap-x-3 rounded-md p-2 text-sm leading-6 font-semibold']">
                        <span class="truncate">{{ team.name }}</span>
                      </a>
                    </li>
                  </ul>
                </div>
                <div class="pt-4">
                  <div class="text-xs font-semibold leading-6 text-gray-300">Recent</div>
                  <ul role="list" class="-mx-2 space-y-1">
                    <li v-for="team in recentLists" :key="team.name">
                      <a :href="team.href" :class="[team.current ? 'bg-gray-800 text-white' : 'text-gray-400 hover:text-white hover:bg-gray-800', 'group flex gap-x-3 rounded-md p-2 text-sm leading-6 font-semibold']">
                        <span class="truncate">{{ team.name }}</span>
                      </a>
                    </li>
                  </ul>
                </div>
                <div class="pt-4">
                  <ul role="list" class="-mx-2 space-y-1">
                    <li>
                      <a href="#" :class="['text-gray-400 hover:text-white hover:bg-gray-800', 'group flex gap-x-3 rounded-md p-2 text-sm leading-6 font-semibold']">
                        <span class="truncate">View All</span>
                      </a>
                    </li>
                  </ul>
                </div>
              </div>
            </li>
            <li>
              <a href="#" :class="['text-gray-400 hover:text-white hover:bg-gray-800', 'group flex gap-x-3 rounded-md p-2 text-sm leading-6 font-semibold']">
                <Squares2X2Icon class="h-6 w-6 shrink-0" aria-hidden="true" />
                Products
              </a>
            </li>
            <li>
              <a href="#" :class="['text-gray-400 hover:text-white hover:bg-gray-800', 'group flex gap-x-3 rounded-md p-2 text-sm leading-6 font-semibold']">
                <BuildingStorefrontIcon class="h-6 w-6 shrink-0" aria-hidden="true" />
                Stores
              </a>
            </li>
          </ul>
        </li>
        <li class="mt-auto flex items-center justify-center">
          <div v-if="isAuthenticated && userStore.me" class="w-full flex flex-row items-center justify-between gap-x-4 py-3">
            <div class="flex flex-row items-center gap-x-4 text-sm font-semibold leading-6 text-white">
              <UserAvatar :user="userStore.me" />
              <span>{{ myFullName }}</span>
            </div>
            <button @click="userStore.logout" type="button" class="rounded-full bg-gray-800 p-1.5 text-white shadow-sm hover:bg-gray-600 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-gray-600">
              <PowerIcon class="h-5 w-5" aria-hidden="true" />
            </button>
          </div>
          <AuthButton v-else class="flex items-center gap-x-4 px-6 py-3" theme="light" />
        </li>
      </ul>
    </nav>
  </div>
</template>

<style scoped>

</style>
