export interface PaginationInterface<T> {
    nextId?: number;
    previousId?: number;
    data: T;
    count: number;
  }