import { createRouter, createWebHistory } from 'vue-router'
import SigninView from '../views/SigninView.vue'
import { useUserStore } from '@/stores/user'
import RouterOnlyView from '@/views/RouterOnlyView.vue'
import ListsView from '@/views/ListsView.vue'
import StoresView from '@/views/StoresView.vue'

export const SIGNIN_ROUTE = 'Signin'
export const LISTS_ROUTE = 'List'
export const LIST_DETAIL_ROUTE = 'ListDetail'
export const PRODUCTS_ROUTE = 'Product'
export const PRODUCT_DETAIL_ROUTE = 'ProductDetail'
export const STORES_ROUTE = 'Store'
export const STORE_DETAIL_ROUTE = 'StoreDetail'

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
      component: RouterOnlyView,
      meta: {
        requiresAuth: true,
      },
      children: [
        {
          path: '',
          name: LISTS_ROUTE,
          component: ListsView,
          props: true,
        },
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
      component: () => import('../views/ProductsView.vue'),
      children: [
        {
          path: ':productId',
          name: PRODUCT_DETAIL_ROUTE,
          component: () => import('../views/ProductDetailView.vue'),
          props: true,
        },
      ],
    },
    {
      path: '/stores',
      component: RouterOnlyView,
      meta: {
        requiresAuth: true,
      },
      children: [
        {
          path: '',
          name: STORES_ROUTE,
          component: StoresView,
          props: true,
        },
        {
          path: ':storeId',
          name: STORE_DETAIL_ROUTE,
          component: () => import('../views/StoreDetailView.vue'),
          props: true,
        },
      ],
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
