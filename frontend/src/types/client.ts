// Types for Client management

export interface Client {
  id: string;
  name: string;
  email?: string;
  phone_number?: string;
  address?: string;
  company_name?: string;
  is_active: boolean;
  created_at: string;
  updated_at?: string;
}

export interface ClientCreate {
  name: string;
  email?: string;
  phone_number?: string;
  address?: string;
  company_name?: string;
  is_active?: boolean;
}

export interface ClientUpdate {
  name?: string;
  email?: string;
  phone_number?: string;
  address?: string;
  company_name?: string;
  is_active?: boolean;
}