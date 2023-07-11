import { ref } from 'vue';
import { defineStore } from 'pinia';
import { useQuery } from "@/api";
import {
  AllProductsDocument,
} from "@/api/gql/graphql";
import { humanizeGraphQLResponse } from '@/utils/graphql';

export const useShopStore = defineStore('shop', () => {
  const products = ref({});

  async function getProducts() {
    const { data } = await useQuery({ query: AllProductsDocument, cachePolicy: "network-only" });
    const processedData = humanizeGraphQLResponse(data?.value);

    console.log(processedData);
  }

  return {
    products,
    getProducts,
  };
});
