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
    const response = await fetch(url, config);
    
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }
    
    return await response.json();
  } catch (error) {
    console.error(`API call failed for ${endpoint}:`, error);
    throw error;
  }
}

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

// Dashboard API functions
export const dashboardAPI = {
  getStats: () => apiCall('/dashboard/stats'),
};

// Other API functions (placeholders for now)
export const clientAPI = {
  getAll: () => apiCall('/clients'),
};

export const orderAPI = {
  getAll: () => apiCall('/orders'),
};

export const inventoryAPI = {
  getAll: () => apiCall('/inventory'),
};