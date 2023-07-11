<script setup lang="ts">
import { computed } from 'vue';
import {
  BuildingStorefrontIcon,
  QueueListIcon,
  Squares2X2Icon,
  PowerIcon,
} from '@heroicons/vue/24/outline'
import { useRoute, RouterLink, type RouteLocationNamedRaw, useRouter } from 'vue-router';
import { useUserStore } from '@/stores/user';
import { getFullName } from '@/utils/user';
import AuthButton from '@/components/AuthButton.vue';
import UserAvatar from '@/components/UserAvatar.vue';
import { LISTS_ROUTE, LIST_DETAIL_ROUTE, PRODUCTS_ROUTE, STORES_ROUTE } from '@/router';

const route = useRoute()
const router = useRouter()
const userStore = useUserStore()
const myFullName = computed(() => {
  return userStore.me ? getFullName(userStore.me) : null
})

const isAuthenticated = computed(() => {
  return userStore.isAuthenticated;
});

function isActiveRoutePath(navRoute: RouteLocationNamedRaw) {
  const resolvedRoute = router.resolve(navRoute);
  return route.matched.some((record) => record.path === resolvedRoute.path);
}

const navigation = [
  {
    name: "Lists",
    icon: QueueListIcon,
    current: false,
    route: { name: LISTS_ROUTE },
    children: [
      {
        name: "Pinned",
        children: [
          {
            name: "Grocery",
            route: { name: LIST_DETAIL_ROUTE, params: { listId: "1" } },
          },
          {
            name: "Home Goods",
            route: { name: LIST_DETAIL_ROUTE, params: { listId: "2" } },
          },
        ],
      },
      {
        name: "Recent",
        children: [
          {
            name: "Grocery",
            route: { name: LIST_DETAIL_ROUTE, params: { listId: "3" } },
          },
          {
            name: "Home Goods",
            route: { name: LIST_DETAIL_ROUTE, params: { listId: "4" } },
          },
        ],
      },
      {
        name: "View all",
        route: { name: LISTS_ROUTE },
        disableActive: true,
      },
    ]
  },
  {
    name: "Products",
    route: { name: PRODUCTS_ROUTE },
    icon: Squares2X2Icon,
  },
  {
    name: "Stores",
    route: { name: STORES_ROUTE },
    icon: BuildingStorefrontIcon,
  },
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
            <li v-for="item in navigation" :key="item.name">
              <RouterLink
                :to="item.route"
                active-class="text-white bg-gray-800"
                class="group flex gap-x-3 rounded-md p-2 text-sm leading-6 font-semibold text-gray-400 hover:bg-gray-800">
                <component :is="item.icon" class="h-6 w-6 shrink-0 text-gray-400" aria-hidden="true" />
                {{ item.name }}
              </RouterLink>
              <div
                v-if="userStore.isAuthenticated && isActiveRoutePath(item.route) && item.children"
                class="divide-y divide-gray-700 space-y-4 p-2"
              >
                <div v-for="childItem in item.children" :key="childItem.name" class="pt-4 first:pt-0">
                  <template v-if="childItem.children">
                    <div class="text-xs font-semibold leading-6 text-gray-300">{{ childItem.name }}</div>
                    <ul role="list" class="-mx-2 space-y-1">
                      <li v-for="grandchildItem in childItem.children" :key="grandchildItem.name">
                        <RouterLink
                          :to="grandchildItem.route"
                          active-class="text-white bg-gray-800"
                          class="text-gray-400 hover:text-white hover:bg-gray-800', 'group flex gap-x-3 rounded-md p-2 text-sm leading-6 font-semibold">
                          <span class="truncate">{{ grandchildItem.name }}</span>
                        </RouterLink>
                      </li>
                    </ul>
                  </template>
                  <template v-else>
                    <ul role="list" class="-mx-2 space-y-1">
                      <li>
                        <RouterLink
                          :to="childItem.route"
                          :active-class="childItem.disableActive ? '' : 'text-white bg-gray-800'"
                          class="text-gray-400 hover:text-white hover:bg-gray-800', 'group flex gap-x-3 rounded-md p-2 text-sm leading-6 font-semibold">
                          <span class="truncate">{{ childItem.name }}</span>
                        </RouterLink>
                      </li>
                    </ul>
                  </template>
                </div>

              </div>
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
