import { ref, type Ref } from 'vue';
import { useLocalStorage } from '@vueuse/core';
import { defineStore } from 'pinia';
import type { IUser } from '@/types/user';
import {
  getMe as getMeReq,
  loginWithGoogle as loginWithGoogleReq,
  logout as logoutReq,
} from '@/api/user';

export const useUserStore = defineStore('user', () => {
  const accessToken: Ref<string | null> = useLocalStorage('shoplist/user/accessToken', null)
  const refreshToken: Ref<string | null> = useLocalStorage('shoplist/user/refreshToken', null)
  const user: Ref<IUser | null> = ref(null)
  const isAuthenticated = ref(false)

  async function getMe() {
    if (!accessToken.value) {
      return;
    }

    const userRes = await getMeReq()

    user.value = userRes

    return user.value;
  }

  async function autoLogin() {
    await getMe()

    if (user.value) {
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
    user.value = null

    window.location.href = '/'
  }


  return {
    accessToken,
    user,
    isAuthenticated,
    autoLogin,
    loginWithGoogle,
    logout,
  }
});
