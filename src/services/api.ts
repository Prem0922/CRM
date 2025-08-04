import axios from 'axios';

// Configure axios to use the correct backend URL and handle errors
axios.defaults.baseURL = 'https://crm-n577.onrender.com';

// Add API key to all requests
axios.defaults.headers.common['x-api-key'] = 'mysecretkey';

// Add response interceptor to handle errors globally
axios.interceptors.response.use(
  (response) => response,
  (error) => {
    console.error('API Error:', error);
    return Promise.reject(error);
  }
);

// Authentication interfaces
export interface SignupData {
  email: string;
  password: string;
  name: string;
}

export interface LoginData {
  email: string;
  password: string;
}

export interface AuthResponse {
  access_token: string;
  token_type: string;
  user_name: string;
}

// Authentication API
export const signup = async (data: SignupData): Promise<AuthResponse> => {
  const response = await axios.post('/auth/signup', data);
  return response.data;
};

export const login = async (data: LoginData): Promise<AuthResponse> => {
  const response = await axios.post('/auth/login', data);
  return response.data;
};

export interface Card {
  id: string;
  type: string;
  status: string;
  balance: number;
  issue_date: string;
  customer_id: string;
}

export interface Customer {
  id: string;
  name: string;
  email: string;
  phone: string;
  notifications: string;
  join_date: string;
}

export interface Trip {
  id: string;  // Trip ID
  start_time: string;
  end_time: string;
  entry_location: string;
  exit_location: string;
  fare: number;
  route: string;
  operator: string;
  transit_mode: string;  // SubWay, Bus, Rail
  adjustable: string;  // Yes, No
  card_id: string;
}

export interface Case {
  id: string;
  customer_id: string;
  card_id: string;
  case_status: string;
  priority: string;
  category: string;
  assigned_agent: string;
  notes: string;
  created_date: string;
  last_updated: string;
}

export interface TapHistoryEntry {
  id: string;
  tap_time: string;
  location: string;
  device_id: string;
  transit_mode: string;
  direction: string;
  customer_id: string;
  result: string;
}

export interface FareDispute {
  id: number;
  dispute_date: string;
  card_id: string;
  amount: number;
  description: string;
  trip_id: string;
  dispute_type: string;
}

// Customer API
export const getCustomers = async () => {
  const response = await axios.get('/customers/');
  return response.data;
};

export const getCustomer = async (id: string) => {
  const response = await axios.get(`/customers/${id}`);
  return response.data;
};

export const createCustomer = async (data: Partial<Customer>) => {
  const response = await axios.post('/customers/', data);
  return response.data;
};

export const updateCustomer = async (id: string, data: Partial<Customer>) => {
  const response = await axios.put(`/customers/${id}`, data);
  return response.data;
};

export const deleteCustomer = async (id: string) => {
  const response = await axios.delete(`/customers/${id}`);
  return response.data;
};

// Card API
export const getCards = async () => {
  const response = await axios.get('/cards/');
  return response.data;
};

export const getCard = async (id: string) => {
  const response = await axios.get(`/cards/${id}`);
  return response.data;
};

export const createCard = async (data: Partial<Card>) => {
  const response = await axios.post('/cards/', data);
  return response.data;
};

export const updateCard = async (id: string, data: Partial<Card>) => {
  const response = await axios.put(`/cards/${id}`, data);
  return response.data;
};

export const deleteCard = async (id: string) => {
  const response = await axios.delete(`/cards/${id}`);
  return response.data;
};

// Trip API
export const getTrips = async () => {
  const response = await axios.get('/trips/');
  return response.data;
};

export const getTrip = async (id: string) => {
  const response = await axios.get(`/trips/${id}`);
  return response.data;
};

export const createTrip = async (data: Partial<Trip>) => {
  const response = await axios.post('/trips/', data);
  return response.data;
};

export const updateTrip = async (id: string, data: Partial<Trip>) => {
  const response = await axios.put(`/trips/${id}`, data);
  return response.data;
};

export const deleteTrip = async (id: string) => {
  const response = await axios.delete(`/trips/${id}`);
  return response.data;
};

// Case API
export const getCases = async () => {
  const response = await axios.get('/cases/');
  return response.data;
};

export const getCase = async (id: string) => {
  const response = await axios.get(`/cases/${id}`);
  return response.data;
};

export const createCase = async (data: Partial<Case>) => {
  const response = await axios.post('/cases/', data);
  return response.data;
};

export const updateCase = async (id: string, data: Partial<Case>) => {
  const response = await axios.put(`/cases/${id}`, data);
  return response.data;
};

export const deleteCase = async (id: string) => {
  const response = await axios.delete(`/cases/${id}`);
  return response.data;
};

// Tap History API
export const getTapHistory = async () => {
  const response = await axios.get('/tap-history/');
  return response.data;
};

export const getTapHistoryByCustomer = async (customerId: string) => {
  const response = await axios.get(`/tap-history/?customer_id=${customerId}`);
  return response.data;
};

export const updateTapHistory = async (id: string, data: Partial<TapHistoryEntry>) => {
  const response = await axios.put(`/tap-history/${id}`, data);
  return response.data;
};

// Fare Dispute API
export const getFareDisputes = async () => {
  const response = await axios.get('/fare-disputes/');
  return response.data;
};

export const gettrips = async () => {
  const response = await axios.get('/trips/');
  return response.data;
};

export const customers = async () => {
  const response = await axios.get('/customers/');
  return response.data;
};

export const createFareDispute = async (data: Partial<FareDispute>) => {
  const response = await axios.post('/fare-disputes/', data);
  return response.data;
};

export const updateFareDispute = async (id: number, data: Partial<FareDispute>) => {
  const response = await axios.put(`/fare-disputes/${id}`, data);
  return response.data;
};

export const deleteFareDispute = async (id: number) => {
  const response = await axios.delete(`/fare-disputes/${id}`);
  return response.data;
};

export { axios }; 