import { computed, ref, type Ref } from 'vue';
import { useLocalStorage } from '@vueuse/core';
import { defineStore } from 'pinia';
import type { IUsers } from '@/types/user';
import {
  getMe as getMeReq,
  loginWithGoogle as loginWithGoogleReq,
  logout as logoutReq,
} from '@/api/user';

export const useUserStore = defineStore('user', () => {
  const accessToken: Ref<string | null> = useLocalStorage('shoplist/user/accessToken', null)
  const refreshToken: Ref<string | null> = useLocalStorage('shoplist/user/refreshToken', null)
  const myId: Ref<string|null> = ref(null)
  const users: Ref<IUsers> = ref({})
  const isAuthenticated = ref(false)

  const me = computed(() => {
    return myId.value ? users.value[myId.value] : null
  })


  async function getMe() {
    if (!accessToken.value) {
      return;
    }

    const meRes = await getMeReq()

    myId.value = meRes.uid
    users.value[myId.value] = meRes

    return me.value
  }

  async function autoLogin() {
    await getMe()

    if (me.value) {
      isAuthenticated.value = true
      return isAuthenticated.value;
    }

    accessToken.value = null
    refreshToken.value = null
    isAuthenticated.value = false
    return isAuthenticated.value;
  }

  async function loginWithGoogle(googleToken: string) {
    const res = await loginWithGoogleReq(googleToken)

    accessToken.value = res.access_token
    refreshToken.value = res.refresh_token
    await getMe()
    isAuthenticated.value = true
  }

  async function logout() {
    await logoutReq()

    isAuthenticated.value = false
    accessToken.value = null
    refreshToken.value = null
    users.value = {}

    window.location.href = '/'
  }


  return {
    accessToken,
    users,
    me,
    isAuthenticated,
    autoLogin,
    loginWithGoogle,
    logout,
  }
});
