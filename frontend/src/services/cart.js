import apiClient from './client';

export async function addToCart(menuItemId, quantity = 1) {
  const response = await apiClient.post('/cart/menu-items/', {
    menuitem: menuItemId,
    quantity,
  });

  return response.data;
}

export async function getCartItems() {
  const response = await apiClient.get('/cart/menu-items/');
  return response.data;
}
