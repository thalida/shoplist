import { createRouter, createWebHistory } from 'vue-router'
import SigninView from '../views/SigninView.vue'
import { useUserStore } from '@/stores/user'
import ListsView from '@/views/ListsView.vue'

export const SIGNIN_ROUTE = 'Signin'
export const LISTS_ROUTE = 'List'
export const LIST_DETAIL_ROUTE = 'ListDetail'
export const PRODUCTS_ROUTE = 'Product'
export const STORES_ROUTE = 'Store'

export const HOME_ROUTE = LISTS_ROUTE

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/signin',
      name: SIGNIN_ROUTE,
      component: SigninView,
      meta: {
        requiresAnon: true,
      },
    },
    {
      alias: '/',
      path: '/lists',
      name: LISTS_ROUTE,
      component: ListsView,
      meta: {
        requiresAuth: true,
      },
      children: [
        {
          path: ':listId',
          name: LIST_DETAIL_ROUTE,
          component: () => import('../views/ListDetailView.vue'),
          props: true,
        },
      ],
    },
    {
      path: '/products',
      name: PRODUCTS_ROUTE,
      meta: {
        requiresAuth: true,
      },
      component: () => import('../views/ProductsView.vue')
    },
    {
      path: '/stores',
      name: STORES_ROUTE,
      meta: {
        requiresAuth: true,
      },
      component: () => import('../views/StoresView.vue')
    },
  ]
})

router.beforeEach(async (to) => {
  const userStore = useUserStore()

  await userStore.autoLogin()

  const isAuthenticated = userStore.isAuthenticated

  const requiresAuth = to.matched.some(record => record.meta.requiresAuth)
  if (requiresAuth && !isAuthenticated) {
    return { name: SIGNIN_ROUTE }
  }

  const requiresAnon = to.matched.some(record => record.meta.requiresAnon)
  if (requiresAnon && isAuthenticated) {
    return { name: HOME_ROUTE }
  }
})


export default router
