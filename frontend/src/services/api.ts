// API service for making HTTP requests to our FastAPI backend

const API_BASE_URL = 'http://localhost:8000/api/v1';

// Generic API call function
async function apiCall(endpoint: string, options: RequestInit = {}) {
  const url = `${API_BASE_URL}${endpoint}`;
  
  const defaultOptions: RequestInit = {
    headers: {
      'Content-Type': 'application/json',
    },
  };

  const config = { ...defaultOptions, ...options };

  try {
    console.log(`Making API call to: ${url}`);
    console.log('Request config:', config);
    
    const response = await fetch(url, config);
    
    console.log(`Response status: ${response.status}`);
    
    if (!response.ok) {
      let errorDetails = `HTTP error! status: ${response.status}`;
      try {
        const errorBody = await response.json();
        console.error('Error response body:', errorBody);
        errorDetails += ` - ${JSON.stringify(errorBody)}`;
      } catch (e) {
        // If we can't parse error response, use the text
        try {
          const errorText = await response.text();
          console.error('Error response text:', errorText);
          errorDetails += ` - ${errorText}`;
        } catch (e2) {
          console.error('Could not read error response');
        }
      }
      throw new Error(errorDetails);
    }
    
    const data = await response.json();
    console.log('Response data:', data);
    return data;
  } catch (error) {
    console.error(`API call failed for ${endpoint}:`, error);
    throw error;
  }
}

// Dashboard API functions
export const dashboardAPI = {
  getStats: () => apiCall('/dashboard/stats'),
  getRecentOrders: () => apiCall('/dashboard/recent-orders'),
  getLowStockAlerts: () => apiCall('/dashboard/low-stock-alerts'),
};

// Deliverer API functions
export const delivererAPI = {
  // Get all deliverers
  getAll: () => apiCall('/deliverers'),
  
  // Get deliverer by ID
  getById: (id: string) => apiCall(`/deliverers/${id}`),
  
  // Create new deliverer
  create: (deliverer: any) => apiCall('/deliverers', {
    method: 'POST',
    body: JSON.stringify(deliverer),
  }),
  
  // Update deliverer
  update: (id: string, deliverer: any) => apiCall(`/deliverers/${id}`, {
    method: 'PUT',
    body: JSON.stringify(deliverer),
  }),
  
  // Delete deliverer
  delete: (id: string) => apiCall(`/deliverers/${id}`, {
    method: 'DELETE',
  }),
  
  // Get stats
  getStats: () => apiCall('/deliverers/stats/summary'),
};

// Client API functions
export const clientAPI = {
  getAll: () => apiCall('/clients'),
  getById: (id: string) => apiCall(`/clients/${id}`),
  create: (client: any) => apiCall('/clients', {
    method: 'POST',
    body: JSON.stringify(client),
  }),
  update: (id: string, client: any) => apiCall(`/clients/${id}`, {
    method: 'PUT',
    body: JSON.stringify(client),
  }),
  delete: (id: string) => apiCall(`/clients/${id}`, {
    method: 'DELETE',
  }),
};

// Order API functions
export const orderAPI = {
  getAll: () => apiCall('/orders'),
  getById: (id: string) => apiCall(`/orders/${id}`),
  create: (order: any) => apiCall('/orders', {
    method: 'POST',
    body: JSON.stringify(order),
  }),
  update: (id: string, order: any) => apiCall(`/orders/${id}`, {
    method: 'PUT',
    body: JSON.stringify(order),
  }),
  delete: (id: string) => apiCall(`/orders/${id}`, {
    method: 'DELETE',
  }),
};

// Inventory API functions
export const inventoryAPI = {
  getAll: () => apiCall('/inventory'),
  getById: (id: string) => apiCall(`/inventory/${id}`),
  create: (item: any) => apiCall('/inventory', {
    method: 'POST',
    body: JSON.stringify(item),
  }),
  update: (id: string, item: any) => apiCall(`/inventory/${id}`, {
    method: 'PUT',
    body: JSON.stringify(item),
  }),
  delete: (id: string) => apiCall(`/inventory/${id}`, {
    method: 'DELETE',
  }),
};