import { createRouter, createWebHistory, routerKey } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import SigninView from '../views/SigninView.vue'
import { useUserStore } from '@/stores/user'

const HOME_ROUTE = 'HomeView'
const SIGNIN_ROUTE = 'SigninView'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: HOME_ROUTE,
      component: HomeView,
      meta: {
        requiresAuth: true,
      },
    },
    {
      path: '/signin',
      name: SIGNIN_ROUTE,
      component: SigninView,
      meta: {
        requiresAnon: true,
      },
    },
    {
      path: '/about',
      name: 'about',
      // route level code-splitting
      // this generates a separate chunk (About.[hash].js) for this route
      // which is lazy-loaded when the route is visited.
      component: () => import('../views/AboutView.vue')
    }
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
