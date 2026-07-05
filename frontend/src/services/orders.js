import apiClient from './client';

export async function createOrder() {
  const response = await apiClient.post('/orders/');
  return response.data;
}
export async function getOrders() {
  const response = await apiClient.get('/orders/');
  return response.data;
}
