export interface Supplier {
  id: string;
  name: string;
  contact_name: string;
  phone_number: string;
  is_active: boolean;      
  email: string;
  phone: string;
  address: string;
  category?: string;
  created_at: string;
}