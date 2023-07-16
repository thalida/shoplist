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
  });
  const pageOrder: Ref<string[]> = ref([]);
  const pageItems = computed(() => {
    const activePage: any[] = [];
    for (const uid of pageOrder.value) {
      activePage.push(collection.value[uid]);
    }
    return activePage;
  });
  const categories: Ref<Record<string, any>> = ref({});
  const categoryOrder: Ref<string[]> = ref([]);


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
      errors.value = JSON.parse(error.value.response.body.errors[0].message);
      pageOrder.value = [];
      isLoading.value = false;
      return;
    }

    errors.value = null;

    const totalCount = data?.value?.allProducts?.totalCount || 0;
    const pageInfoRes = data?.value?.allProducts?.pageInfo;
    const productsRes = humanizeGraphQLResponse(data?.value);

    pageInfo.value = {
      hasPreviousPage: pageInfoRes?.hasPreviousPage || false,
      hasNextPage: pageInfoRes?.hasNextPage || false,
      startCursor: pageInfoRes?.startCursor || "",
      endCursor: pageInfoRes?.endCursor || "",
      totalCount,
    }

    if (!productsRes) {
      pageOrder.value = [];
      isLoading.value = false;
      return;
    }

    const newPageOrder: string[] = [];
    for (const product of productsRes.allProducts) {
      collection.value[product.uid] = product;
      newPageOrder.push(product.uid);
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

    categories.value = {};
    categoryOrder.value = [];
    for (const category of res.allProductCategories) {
      categories.value[category.uid] = category;
      categoryOrder.value.push(category.uid);
    }
  }

  return {
    collection,
    isLoading,
    errors,
    pageItems,
    pageInfo,
    orderBy,
    filterBy,
    getById,
    getOrFetch,
    fetch,

    categories,
    categoryOrder,
    getCategories,

    setOrderBy,
    setFilterBy,
  };
});
