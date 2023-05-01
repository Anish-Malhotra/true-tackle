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
  pageParam,
}: QueryFunctionContext<QueryKeyT>): Promise<T> => {
  const [url, size] = queryKey;
  console.log(`page: ${pageParam}`)
  console.log(`size: ${size}`)
  const urlWithQueryKeys = `${url}?page=${pageParam}&size=${size}`;
  return api
    .get<T>(urlWithQueryKeys)
    .then((res) => res.data);
};

export const useLoadMore = <T>(url: string | null, size = 1) => {
  const context = useInfiniteQuery<
    PaginationInterface<T>,
    Error,
    PaginationInterface<T>,
    QueryKeyT
  >(
    [url!, size!],
    ({ queryKey, pageParam = 1 }) => fetcher({ queryKey, pageParam }),
    {
      getPreviousPageParam: (firstPage) => firstPage.previous_id ?? false,
      getNextPageParam: (lastPage) => {
        return lastPage.next_id;
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
