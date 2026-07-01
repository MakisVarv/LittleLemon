import apiClient from './client';

export async function getMenuItems() {
  const response = await apiClient.get('/menu-items/');
  return response.data;
}
