export interface Supplier {
  id: string;
  name: string;
  contact_person?: string;
  phone_number?: string;
  is_active: boolean;      
  email?: string;
  address?: string;
  category?: string;
  created_at: string;
  updated_at: string;
}