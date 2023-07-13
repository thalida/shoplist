import { computed, ref, type Ref } from 'vue';
import { defineStore } from 'pinia';
import { useQuery } from "@/api";
import {
  AllProductsDocument, type QueryAllProductsArgs,
} from "@/api/gql/graphql";
import { humanizeGraphQLResponse } from '@/utils/graphql';
import type { IPageInfo, IOrderBy, IFilterBy, IError } from '@/types/graphql';
import { cloneDeep } from 'lodash';

export const useShopStore = defineStore('shop', () => {
  const products: Ref<Record<string, any>> = ref({});
  const productsIsLoading: Ref<boolean> = ref(false);
  const productsAPIErrors: Ref<IError | null> = ref(null);
  const productsPageInfo: Ref<IPageInfo> = ref({
    hasNextPage: false,
    hasPreviousPage: false,
    startCursor: "",
    endCursor: "",
    totalCount: 0,
  });
  const productsOrderBy: Ref<IOrderBy> = ref({});
  const productsFilterBy: Ref<IFilterBy> = ref({});
  const productsPageOrder: Ref<string[]> = ref([]);
  const productsPageItems = computed(() => {
    const activePage: any[] = [];
    for (const uid of productsPageOrder.value) {
      activePage.push(products.value[uid]);
    }
    return activePage;
  });

  async function getProducts(args?: QueryAllProductsArgs) {
    productsIsLoading.value = true;

    const { data, error } = await useQuery({
      query: AllProductsDocument,
      variables: args,
      cachePolicy: "network-only"
    });

    if (error.value) {
      productsAPIErrors.value = error.value;
      productsPageOrder.value = [];
      productsIsLoading.value = false;
      return;
    }


    const totalCount = data?.value?.allProducts?.totalCount || 0;
    const pageInfo = data?.value?.allProducts?.pageInfo;
    const productsRes = humanizeGraphQLResponse(data?.value);

    productsPageInfo.value = {
      hasPreviousPage: pageInfo?.hasPreviousPage || false,
      hasNextPage: pageInfo?.hasNextPage || false,
      startCursor: pageInfo?.startCursor || "",
      endCursor: pageInfo?.endCursor || "",
      totalCount,
    }

    if (!productsRes) {
      productsPageOrder.value = [];
      productsIsLoading.value = false;
      return;
    }

    const newPageOrder: string[] = [];
    for (const product of productsRes.allProducts) {
      products.value[product.uid] = product;
      newPageOrder.push(product.uid);
    }

    productsPageOrder.value = newPageOrder;
    productsIsLoading.value = false;
  }

  function formatOrderByArgs(orderBy: IOrderBy | null | undefined) {
    if (typeof orderBy === "undefined" || orderBy === null) {
      return "";
    }

    const orderByStr = Object.keys(orderBy).map((key) => {
      const value = orderBy[key];
      if (value === null) {
        return
      }
      return `${value ? "" : "-"}${key}`;
    }).join(", ");

    return orderByStr;
  }

  function toggleOrderByField(orderBy: IOrderBy, field: string) {
    const hasKey = Object.keys(orderBy).includes(field);

    if (hasKey) {
      orderBy[field] = !orderBy[field];
    } else {
      orderBy[field] = true;
    }
  }

  return {
    products,
    productsIsLoading,
    productsAPIErrors,
    productsPageItems,
    productsPageInfo,
    productsOrderBy,
    productsFilterBy,
    getProducts,

    formatOrderByArgs,
    toggleOrderByField,
  };
});
