import axios from 'axios';

export const api = {
  get: <T>(url: string, params?: object) =>
    axios.get<T>(url, {
      ...params,
    }),
};