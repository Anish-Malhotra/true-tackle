// @ts-nocheck

import { api } from './api';
import {
  useInfiniteQuery,
  useQuery,
  UseQueryOptions,
} from 'react-query';
import { QueryFunctionContext } from 'react-query/types/core/types';
import { PaginationInterface } from '../interfaces';

type QueryKeyT = [string, object | undefined];

export const fetcher = <T>({
  queryKey,
  page,
  size,
}: QueryFunctionContext<QueryKeyT>): Promise<T> => {
  const [url, params] = queryKey;
  return api
    .get<T>(url, { params: { ...params, page, size } })
    .then((res: { data: any; }) => res.data);
};

export const useLoadMore = <T>(url: string | null, params?: object) => {
  const context = useInfiniteQuery<
    PaginationInterface<T>,
    Error,
    PaginationInterface<T>,
    QueryKeyT
  >(
    [url!, params],
    ({ queryKey, page = 1, size = 20 }) => fetcher({ queryKey, page, size }),
    {
      getPreviousPageParam: (firstPage) => firstPage.previousId ?? false,
      getNextPageParam: (lastPage) => {
        return lastPage.nextId ?? false;
      },
    }
  );

  return context;
};

export const useFetch = <T>(
  url: string | null,
  params?: object,
  config?: UseQueryOptions<T, Error, T, QueryKeyT>
) => {
  const context = useQuery<T, Error, T, QueryKeyT>(
    [url!, params],
    ({ queryKey }) => fetcher({ queryKey }),
    {
      enabled: !!url,
      ...config,
    }
  );

  return context;
};
