 // Types for Order management

export interface Order {
  id: string;
  order_number: string;
  client_id: string;
  client_name?: string;
  reseller_id?: string;
  deliverer_id?: string;
  deliverer_name?: string;
  status: OrderStatus;
  order_date: string;
  delivery_date?: string;
  delivery_address: string;
  total_amount: number;
  notes?: string;
  items: OrderItem[];
  created_at: string;
  updated_at?: string;
}

export interface OrderItem {
  id?: string;
  product_name: string;
  quantity: number;
  unit_price: number;
  total_price: number;
}

export interface OrderCreate {
  order_number: string;
  client_id: string;
  reseller_id?: string;
  deliverer_id?: string;
  status?: OrderStatus;
  order_date: string;
  delivery_date?: string;
  delivery_address: string;
  total_amount: number;
  notes?: string;
  items: OrderItem[];
}

export interface OrderUpdate {
  client_id?: string;
  deliverer_id?: string;
  status?: OrderStatus;
  order_date?: string;
  delivery_date?: string;
  delivery_address?: string;
  total_amount?: number;
  notes?: string;
  items?: OrderItem[];
}

export type OrderStatus = 
  | 'pending'
  | 'confirmed'
  | 'in_transit'
  | 'delivered'
  | 'cancelled';

export const ORDER_STATUS_OPTIONS: { value: OrderStatus; label: string; color: string }[] = [
  { value: 'pending', label: 'Pending', color: 'bg-yellow-100 text-yellow-800' },
  { value: 'confirmed', label: 'Confirmed', color: 'bg-blue-100 text-blue-800' },
  { value: 'in_transit', label: 'In Transit', color: 'bg-purple-100 text-purple-800' },
  { value: 'delivered', label: 'Delivered', color: 'bg-green-100 text-green-800' },
  { value: 'cancelled', label: 'Cancelled', color: 'bg-red-100 text-red-800' }
];