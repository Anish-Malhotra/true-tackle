export const API_BASE_URL = 'http://localhost:5001';

export const apiRoutes = {
    getOrdersList: API_BASE_URL + '/api/v1/orders',
    getOrdersRevenue: API_BASE_URL + '/api/v1/orders/revenue',
    getProductsList: API_BASE_URL + '/api/v1/products',
    getVendorsList: API_BASE_URL + '/api/v1/vendors',
    getOrder: API_BASE_URL + '/api/v1/orders/:id',
    getProduct: API_BASE_URL + '/api/v1/products/:id',
    getVendor: API_BASE_URL + '/api/v1/vendor/:id',
};

export const DEFAULT_PAGE_SIZE = 5;