import apiClient from './client';

export async function getDeliveryCrewUsers() {
  const response = await apiClient.get(
    '/groups/delivery-crew/users/',
  );
  return response.data;
}
