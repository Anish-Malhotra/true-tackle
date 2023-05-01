export interface PaginationInterface<T> {
    next_id?: number;
    prev_id?: number;
    data: T;
    count: number;
  }