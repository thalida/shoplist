import { ref, type Ref } from 'vue';
import { defineStore } from 'pinia';
import { useQuery } from "@/api";;
import { AllPantriesDocument } from '@/api/gql/graphql';
import { humanizeGraphQLResponse } from '@/utils/api';
import { cloneDeep } from 'lodash';

export const usePantryStore = defineStore('pantry', () => {
  const pantry: Ref<Record<string, any> | null> = ref(null);

  async function fetchPantry() {
    const { data } = await useQuery({ query: AllPantriesDocument });

    const res = humanizeGraphQLResponse(data?.value);

    if (!res) {
      pantry.value = null;
      return;
    }

    pantry.value = cloneDeep(res.allPantries[0]);
  }

  return {
    pantry,
    fetchPantry,
  };
});
