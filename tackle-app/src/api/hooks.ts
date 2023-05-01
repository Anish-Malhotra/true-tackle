import {
    useFetch,
    useLoadMore,
} from '../util/reactQuery';
import { apiRoutes } from '../routes';
import {
    Vendor,
    Product,
    Order,
} from '../interfaces/interfaces';
import { pathToUrl } from '../util/router';
  
export const useGetOrdersList = (product_id: number | null, size?: number) =>
    useLoadMore<Order[]>(
        product_id ? pathToUrl(apiRoutes.getProductsList, { product_id }) : apiRoutes.getOrdersList,
        size!,
    );

export const useGetProductsList = (page?: number | null, size?: number) => 
    useLoadMore<Product[]>(
        apiRoutes.getProductsList,
        size!,
    );

export const useGetVendorsList = () => useLoadMore<Vendor[]>(apiRoutes.getVendorsList, 1);

export const useGetOrder = (id: number | null) => 
    useFetch<Order>(
        id ? pathToUrl(apiRoutes.getOrder, { id }) : null
    );

export const useGetProduct = (id: number | null) => 
    useFetch<Product>(
        id ? pathToUrl(apiRoutes.getProduct, { id }) : null
    );

export const useGetVendor = (id: number | null) =>
    useFetch<Vendor>(
            id ? pathToUrl(apiRoutes.getVendor, { id }) : null
    );