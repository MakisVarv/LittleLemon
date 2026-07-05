import apiClient from './client';

export async function loginUser(credentials) {
  const response = await apiClient.post(
    '/auth/token/login/',
    credentials,
  );
  return response.data;
}

export async function logoutUser() {
  const response = await apiClient.post('/auth/token/logout/');
  return response.data;
}

export async function registerUser(userData) {
  const response = await apiClient.post('/auth/users/', userData);
  return response.data;
}

export async function getCurrentUser() {
  const response = await apiClient.get('/users/me/');
  return response.data;
}
