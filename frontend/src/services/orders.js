import apiClient from './client';

export async function createOrder() {
  const response = await apiClient.post('/orders/');
  return response.data;
}
export async function getOrders() {
  const response = await apiClient.get('/orders/');
  return response.data;
}
export async function updateOrderStatus(orderId, status) {
  const response = await apiClient.patch(`/orders/${orderId}/`, {
    status,
  });

  return response.data;
}
export async function assignDeliveryCrew(orderId, deliveryCrewId) {
  const response = await apiClient.patch(`/orders/${orderId}/`, {
    delivery_crew: deliveryCrewId,
  });

  return response.data;
}
