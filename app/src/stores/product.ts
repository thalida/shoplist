import { computed, ref, type Ref } from 'vue';
import { defineStore } from 'pinia';
import { useQuery } from "@/api";
import {
  ProductDocument,
  AllProductsDocument,
  type QueryAllProductsArgs,
  AllProductCategoriesDocument,
} from "@/api/gql/graphql";
import { humanizeGraphQLResponse } from '@/utils/api';
import type { IPageInfo, IOrderBy, IFilterBy, IError } from '@/types/api';
import { cloneDeep } from 'lodash';

export const useProductStore = defineStore('product', () => {
  const collection: Ref<Record<string, any>> = ref({});
  const isLoading: Ref<boolean> = ref(false);
  const errors: Ref<IError | null> = ref(null);
  const pageInfo: Ref<IPageInfo> = ref({
    hasNextPage: false,
    hasPreviousPage: false,
    startCursor: "",
    endCursor: "",
    totalCount: 0,
  });
  const orderBy: Ref<IOrderBy[]> = ref([]);
  const filterBy: Ref<IFilterBy> = ref({
    name_Icontains: null,
    categories: [],
    lists: [],
    stores: [],
  });
  const pageOrder: Ref<string[]> = ref([]);
  const pageItems = computed(() => {
    const activePage: any[] = [];
    for (const uid of pageOrder.value) {
      activePage.push(collection.value[uid]);
    }
    return activePage;
  });
  const categories: Ref<Record<string, any>[]> = ref([]);


  function setOrderBy(newOrderBy: IOrderBy[]) {
    orderBy.value = cloneDeep(newOrderBy);
  }

  function setFilterBy(newFilterBy: IFilterBy) {
    filterBy.value = cloneDeep(newFilterBy);
  }

  function getById(uid: string) {
    return collection.value[uid];
  }

  async function getOrFetch(uid: string) {
    if (uid in collection.value && collection.value[uid] !== null) {
      return getById(uid)
    }

    await fetchOne(uid);
    return getById(uid)
  }

  async function fetchOne(uid: string) {
    const { data, error } = await useQuery({
      query: ProductDocument,
      variables: { uid },
    });

    if (error.value) {
      // productAPIErrors.value = JSON.parse(error.value.response.body.errors[0].message);
      return;
    }

    const res = humanizeGraphQLResponse(data?.value);

    if (!res) {
      return;
    }

    collection.value[res.product.uid] = res.product;
  }

  async function fetch(args?: QueryAllProductsArgs) {
    isLoading.value = true;

    const { data, error } = await useQuery({
      query: AllProductsDocument,
      variables: args,
      cachePolicy: "network-only"
    });

    if (error.value) {
      errors.value = error.value.response.body.errors
      pageOrder.value = [];
      isLoading.value = false;
      return;
    }

    errors.value = null;

    const totalCount = data?.value?.allProducts?.totalCount || 0;
    const pageInfoRes = data?.value?.allProducts?.pageInfo;
    const res = humanizeGraphQLResponse(data?.value);

    pageInfo.value = {
      hasPreviousPage: pageInfoRes?.hasPreviousPage || false,
      hasNextPage: pageInfoRes?.hasNextPage || false,
      startCursor: pageInfoRes?.startCursor || "",
      endCursor: pageInfoRes?.endCursor || "",
      totalCount,
    }

    if (!res) {
      pageOrder.value = [];
      isLoading.value = false;
      return;
    }

    const newPageOrder: string[] = [];
    for (const item of res.allProducts) {
      collection.value[item.uid] = item;
      newPageOrder.push(item.uid);
    }

    pageOrder.value = newPageOrder;
    isLoading.value = false;
  }

  async function getCategories() {
    const { data } = await useQuery({
      query: AllProductCategoriesDocument,
      variables: {
        orderBy: 'name',
      },
    });

    const res = humanizeGraphQLResponse(data?.value);

    if (!res) {
      return;
    }

    categories.value = cloneDeep(res.allProductCategories);
  }

  function getCategoryById (uid: string) {
    return categories.value.find((category) => category.uid === uid);
  }

  return {
    collection,
    isLoading,
    errors,
    pageItems,
    pageOrder,
    pageInfo,
    orderBy,
    filterBy,
    getById,
    getOrFetch,
    fetch,

    categories,
    getCategories,
    getCategoryById,

    setOrderBy,
    setFilterBy,
  };
});
