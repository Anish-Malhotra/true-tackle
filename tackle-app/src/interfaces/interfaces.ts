export interface Product {
    id: number;
    vendor_id: number;
    created_at: string;
    title: string;
    listing_type: string;
    price: number;
}

export interface Order {
    id: number;
    product_id: number;
    created_at: string;
    full_name: string;
    order_date: string;
    quantity: number;
}

export interface Vendor {
    id: number;
    created_at: string;
    name: number;
}
