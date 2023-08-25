import { computed, ref, type Ref } from 'vue';
import { defineStore } from 'pinia';
import { useMutation, useQuery } from "@/api";
import {
  ProductDocument,
  AllProductsDocument,
  type QueryAllProductsArgs,
  AllProductCategoriesDocument,
  CreateProductDocument,
  type CreateProductInput,
  UpdateProductDocument,
  type UpdateProductInput,
  DeleteProductDocument,
  type DeleteProductInput,
  AllProductUnitsDocument,
  CreateProductCategoryDocument,
  type CreateProductCategoryInput,
} from "@/api/gql/graphql";
import { formatOrderByArgs, humanizeGraphQLResponse } from '@/utils/api';
import type { IPageInfo, IOrderBy, IFilterBy, IError } from '@/types/api';
import { cloneDeep } from 'lodash';

export const useProductStore = defineStore('product', () => {
  const collection: Ref<Record<string, any>> = ref({});
  const isLoading: Ref<boolean> = ref(false);
  const errors: Ref<IError | null> = ref(null);
  const pageSize: Ref<number> = ref(5);
  const pageInfo: Ref<IPageInfo> = ref({
    hasNextPage: false,
    hasPreviousPage: false,
    startCursor: "",
    endCursor: "",
    totalCount: 0,
    filteredCount: 0,
  });
  const orderBy: Ref<IOrderBy[]> = ref([]);
  const filterBy: Ref<IFilterBy> = ref({
    name_Icontains: null,
    categories: [],
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
  const units: Ref<Record<string, any>[]> = ref([]);
  const categories: Ref<Record<string, any>[]> = ref([]);
  const lastFetchQuery: Ref<any | null> = ref(null);


  function setOrderBy(newOrderBy: IOrderBy[]) {
    orderBy.value = cloneDeep(newOrderBy);
  }

  function setFilterBy(newFilterBy: IFilterBy) {
    filterBy.value = cloneDeep(newFilterBy);
  }

  function getById(uid: string) {
    return collection.value[uid];
  }

  function getCategoryById (uid: string) {
    return categories.value.find((category) => category.uid === uid);
  }

  function getUnitById (uid: string) {
    return units.value.find((unit) => unit.uid === uid);
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

    const orderByStr = formatOrderByArgs(orderBy.value, { category: 'category__name' });
    const queryArgs: QueryAllProductsArgs = {
      ...args,
      orderBy: orderByStr,
      ...filterBy.value,
    };

    const { data, error, execute } = await useQuery({
      query: AllProductsDocument,
      variables: queryArgs,
    });

    processFetchResponse(data.value, error.value);

    isLoading.value = false;
    lastFetchQuery.value = execute;
  }

  async function refetch() {
    if (!lastFetchQuery.value) {
      return;
    }

    isLoading.value = true;

    const { data, error } = await lastFetchQuery.value();
    processFetchResponse(data, error);

    isLoading.value = false;
  }

  function processFetchResponse(data: any | null, error: any | null) {
    if (error) {
      errors.value = error.response.body.errors
      pageOrder.value = [];
      isLoading.value = false;
      return;
    }

    errors.value = null;

    const totalCount = data?.allProducts?.totalCount || 0;
    const filteredCount = data?.allProducts?.filteredCount || 0;
    const pageInfoRes = data?.allProducts?.pageInfo;
    const res = humanizeGraphQLResponse(data);

    pageInfo.value = {
      hasPreviousPage: pageInfoRes?.hasPreviousPage || false,
      hasNextPage: pageInfoRes?.hasNextPage || false,
      startCursor: pageInfoRes?.startCursor || "",
      endCursor: pageInfoRes?.endCursor || "",
      totalCount,
      filteredCount,
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
  }

  async function fetchCategories() {
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

  async function fetchUnits() {
    const { data } = await useQuery({
      query: AllProductUnitsDocument,
      variables: {
        orderBy: 'name',
      },
    });

    const res = humanizeGraphQLResponse(data?.value);

    if (!res) {
      return;
    }

    units.value = cloneDeep(res.allProductUnits);
  }

  async function create(productData: CreateProductInput) {
    const { execute, data } = useMutation(CreateProductDocument);
    await execute(productData)

    const res = humanizeGraphQLResponse(data?.value)
    if (!res) {
      return;
    }

    collection.value[res.createProduct.product.uid] = res.createProduct.product;
  }

  async function update(productData: UpdateProductInput) {
    const { execute, data } = useMutation(UpdateProductDocument);
    await execute(productData);

    const res = humanizeGraphQLResponse(data?.value)
    if (!res) {
      return;
    }

    collection.value[res.updateProduct.product.uid] = res.updateProduct.product;
  }

  async function createOrUpdate(productData: any): Promise<void> {
    const newCategories = productData.categories
      .filter((category: any) => {
        return typeof category !== 'string';
      })

    if (newCategories.length > 0) {
      const createdCategories = await Promise.all(newCategories.map((category: CreateProductCategoryInput) => {
        return createCategory({
          name: category.name,
          color: category.color,
        })
      }));

      productData.categories = [
        ...productData.categories.filter((category: any) => typeof category === 'string'),
        ...createdCategories.map((category: any) => category.uid),
      ];
    }

    const stores = productData.stores
      .filter((storeProduct: any) => {
        return !storeProduct.shouldRemove && typeof storeProduct.store === 'string';
      })
      .map((storeProduct: any) => {
        return JSON.stringify({
          store: storeProduct.store,
          section: storeProduct.section,
          price: storeProduct.price,
        });
      })

    const formattedProduct = {
      ...productData,
      stores,
    };

    if (formattedProduct.uid === null) {
      return create(formattedProduct)
    } else {
      return update(formattedProduct);
    }
  }

  async function remove(productData: DeleteProductInput) {
    const { execute, data } = useMutation(DeleteProductDocument);
    await execute(productData);

    const res = humanizeGraphQLResponse(data?.value)
    if (!res) {
      return;
    }

    collection.value[res.deleteProduct.product.uid].isDeleted = true;
  }

  async function createCategory(category: CreateProductCategoryInput) {
    const { execute, data } = useMutation(CreateProductCategoryDocument);
    await execute(category);

    const res = humanizeGraphQLResponse(data?.value)
    if (!res) {
      return;
    }

    categories.value.push(res.createProductCategory.productCategory);

    return res.createProductCategory.productCategory;
  }

  return {
    collection,
    isLoading,
    errors,
    pageItems,
    pageOrder,
    pageSize,
    pageInfo,
    orderBy,
    filterBy,
    getById,
    getOrFetch,
    fetch,
    refetch,

    categories,
    fetchCategories,
    getCategoryById,

    units,
    fetchUnits,
    getUnitById,

    setOrderBy,
    setFilterBy,

    create,
    update,
    createOrUpdate,
    remove,

    createCategory,
  };
});
