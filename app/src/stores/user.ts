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

  function setupMyUser() {
    isAuthenticated.value = typeof accessToken.value !== "undefined" && accessToken.value !== null;

    if (isAuthenticated.value) {
      return myId.value ? me.value : fetchMe();
    }

    if (myId.value) {
      delete users.value[myId.value];
    }
    myId.value = null;
  }

  async function autoLogin() {
    if (accessToken.value) {
      const mutation = useMutation(VerifyTokenDocument);

      await mutation.execute({ token: accessToken.value });

      if (mutation.error.value) {
        accessToken.value = null;
      }
    }

    setupMyUser()
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
    setupMyUser();
  }

  function logout() {
    accessToken.value = null;
    setupMyUser();
    window.location.href = "/";
  }

  async function fetchMe() {
    const { data } = await useQuery({ query: MeDocument });
    if (data.value?.me) {
      const user = data.value.me;
      myId.value = user.uid;
      users.value[user.uid] = user;
    }

    return me.value;
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
});
