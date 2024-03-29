// @ts-nocheck

import { api } from './api';
import {
  useInfiniteQuery,
  useQuery,
  UseQueryOptions,
} from 'react-query';
import { QueryFunctionContext } from 'react-query/types/core/types';
import { PaginationInterface } from '../interfaces';
import { DEFAULT_PAGE_SIZE } from '../routes';

type QueryKeyT = [string, object | undefined];

export const fetcher = <T>({
  queryKey,
  pageParam,
}: QueryFunctionContext<QueryKeyT>): Promise<T> => {
  const [url, params, size] = queryKey;
  let urlWithQueryKeys = `${url}?page=${pageParam}&size=${size}`;

  _.forEach(params, (value, key) => {
    urlWithQueryKeys = urlWithQueryKeys.concat(`&${key}=${value}`);
  })

  return api
    .get<T>(urlWithQueryKeys)
    .then((res) => res.data);
};

export const useLoadMore = <T>(url: string | null, size = DEFAULT_PAGE_SIZE, params? = {}) => {
  const context = useInfiniteQuery<
    PaginationInterface<T>,
    Error,
    PaginationInterface<T>,
    QueryKeyT
  >(
    [url!, params!, size!],
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
