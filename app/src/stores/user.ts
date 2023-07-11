import { computed, ref, type Ref } from 'vue';
import { useLocalStorage } from '@vueuse/core';
import { defineStore } from 'pinia';
import { useQuery } from "@/api";
import { useMutation } from "villus";
import {
  MeDocument,
  RegisterSocialDocument,
  VerifyTokenDocument,
} from "@/api/gql/graphql";
import type { IUsers } from '@/types/user';

export const useUserStore = defineStore('user', () => {
  const accessToken = useLocalStorage("shoplist:accessToken", null as string | null | undefined);
  const myId: Ref<string|null> = ref(null)
  const users: Ref<IUsers> = ref({})
  const isAuthenticated = ref(false);

  const me = computed(() => {
    return myId.value ? users.value[myId.value] : null
  })

  function setIsAuthenticated() {
    isAuthenticated.value = typeof accessToken.value !== "undefined" && accessToken.value !== null;

    if (isAuthenticated.value) {
      fetchMe();
    } else if (myId.value !== null) {
      delete users.value[myId.value];
      myId.value = null;
    }
  }

  async function autoLogin() {
    if (accessToken.value) {
      const mutation = useMutation(VerifyTokenDocument);

      await mutation.execute({ token: accessToken.value });

      if (mutation.error.value) {
        accessToken.value = null;
      }
    }

    setIsAuthenticated()
  }

  async function loginWithSocial({
    socialAccessToken,
    socialBackend,
  }: {
    socialAccessToken: string;
    socialBackend: string;
  }) {
    const { data, execute } = useMutation(RegisterSocialDocument);
    await execute({ socialAccessToken, socialBackend });
    accessToken.value = data?.value?.registerSocial?.token;
    setIsAuthenticated();
  }

  function logout() {
    accessToken.value = null;
    setIsAuthenticated();
  }

  async function fetchMe() {
    const { data } = await useQuery({ query: MeDocument, cachePolicy: "network-only" });
    console.log("fetchMe", data.value)
    if (data.value?.me) {
      const user = data.value.me;
      myId.value = user.uid;
      users.value[user.uid] = user;
    }
  }


  return {
    isAuthenticated,
    users,
    me,
    accessToken,
    autoLogin,
    loginWithSocial,
    logout,
  };



  // const accessToken: Ref<string | null> = useLocalStorage('shoplist/user/accessToken', null)
  // const refreshToken: Ref<string | null> = useLocalStorage('shoplist/user/refreshToken', null)
  // const myId: Ref<string|null> = ref(null)
  // const users: Ref<IUsers> = ref({})
  // const isAuthenticated = ref(false)

  // const me = computed(() => {
  //   return myId.value ? users.value[myId.value] : null
  // })

  // function setIsAuthenticated() {
  //   isAuthenticated.value = typeof accessToken.value !== "undefined" && accessToken.value !== null;
  // }


  // async function getMe() {
  //   if (!accessToken.value) {
  //     return;
  //   }

  //   try {
  //     const meRes = await getMeReq()
  //     myId.value = meRes.uid
  //     users.value[myId.value] = meRes
  //   } catch (e) {
  //     myId.value = null
  //   }

  //   return me.value
  // }

  // // async function autoLogin() {
  // //   if (me.value) {
  // //     return isAuthenticated.value;
  // //   }

  // //   await getMe()
  // //   if (me.value) {
  // //     isAuthenticated.value = true
  // //     return isAuthenticated.value;
  // //   }

  // //   accessToken.value = null
  // //   refreshToken.value = null
  // //   isAuthenticated.value = false
  // //   return isAuthenticated.value;
  // // }



  // async function autoLogin() {
  //   if (accessToken.value) {
  //     const mutation = useMutation(VerifyTokenDocument);
  //     isFetching.verifyToken = mutation.isFetching;

  //     await mutation.execute({ token: accessToken.value });

  //     if (mutation.data.value?.verifyToken?.payload) {
  //       isAuthenticated.value = true;
  //     } else {
  //       accessToken.value = null;
  //       isAuthenticated.value = false;
  //     }
  //   }
  // }

  // async function loginWithGoogle(googleToken: string) {
  //   const res = await loginWithGoogleReq(googleToken)

  //   accessToken.value = res.access_token
  //   refreshToken.value = res.refresh_token
  //   await getMe()

  //   isAuthenticated.value = true
  //   router.push({ name: HOME_ROUTE })
  // }

  // async function logout() {
  //   await logoutReq()

  //   isAuthenticated.value = false
  //   accessToken.value = null
  //   refreshToken.value = null
  //   users.value = {}

  //   window.location.href = '/'
  // }


  // return {
  //   accessToken,
  //   users,
  //   me,
  //   isAuthenticated,
  //   autoLogin,
  //   loginWithGoogle,
  //   logout,
  // }
});
