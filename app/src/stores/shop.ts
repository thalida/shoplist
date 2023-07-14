import { computed, ref, type Ref } from 'vue';
import { defineStore } from 'pinia';
import { useQuery } from "@/api";
import {
  AllProductsDocument,
  type QueryAllProductsArgs,
  AllProductCategoriesDocument,
} from "@/api/gql/graphql";
import { humanizeGraphQLResponse } from '@/utils/graphql';
import type { IPageInfo, IOrderBy, IFilterBy, IError } from '@/types/graphql';
import { cloneDeep, findIndex } from 'lodash';

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
  const productsOrderBy: Ref<IOrderBy[]> = ref([]);
  const productsFilterBy: Ref<IFilterBy> = ref({
    name_Icontains: null,
    categories: [],
  });
  const productsPageOrder: Ref<string[]> = ref([]);
  const productsPageItems = computed(() => {
    const activePage: any[] = [];
    for (const uid of productsPageOrder.value) {
      activePage.push(products.value[uid]);
    }
    return activePage;
  });
  const productCategories: Ref<Record<string, any>> = ref({});
  const productCategoryOrder: Ref<string[]> = ref([]);

  async function getProducts(args?: QueryAllProductsArgs) {
    productsIsLoading.value = true;

    const { data, error } = await useQuery({
      query: AllProductsDocument,
      variables: args,
      cachePolicy: "network-only"
    });

    if (error.value) {
      productsAPIErrors.value = JSON.parse(error.value.response.body.errors[0].message);
      productsPageOrder.value = [];
      productsIsLoading.value = false;
      return;
    }

    productsAPIErrors.value = null;

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

  async function getProductCategories() {
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

    productCategories.value = {};
    productCategoryOrder.value = [];
    for (const category of res.allProductCategories) {
      productCategories.value[category.uid] = category;
      productCategoryOrder.value.push(category.uid);
    }
  }


  function formatOrderByArgs(orderBy: IOrderBy[] | null | undefined, keyMap: Record<string, string> = {}) {
    if (typeof orderBy === "undefined" || orderBy === null) {
      return "";
    }

    const orderByStr = orderBy.map((order) => {
      const queryKey = keyMap[order.field] || order.field

      if (order.value === null) {
        return '';
      }

      return `${order.value ? "" : "-"}${queryKey}`;
    }).join(",");

    return orderByStr;
  }

  function setProductsOrderBy(orderBy: IOrderBy[]) {
    productsOrderBy.value = cloneDeep(orderBy);
  }

  function toggleOrderByField(orderBy: IOrderBy[], field: string) {
    const index = findIndex(orderBy, { field })
    const currOrder = orderBy[index]
    const newOrder: IOrderBy = {
      field,
      value: null
    }

    if (typeof currOrder === 'undefined' || currOrder.value === null) {
      newOrder.value = true
    } else if (currOrder.value === true) {
      newOrder.value = false
    } else if (currOrder.value === false) {
      newOrder.value = null
    }

    orderBy = orderBy.filter((order) => order.field !== field)
    orderBy.unshift(newOrder)

    return orderBy
  }

  function setProductsFilterBy(filterBy: IFilterBy) {
    productsFilterBy.value = cloneDeep(filterBy);
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

    productCategories,
    productCategoryOrder,
    getProductCategories,

    setProductsOrderBy,
    setProductsFilterBy,

    formatOrderByArgs,
    toggleOrderByField,
  };
});
