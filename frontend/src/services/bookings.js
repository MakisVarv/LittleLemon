import apiClient from './client';

export async function getBookingAvailability(date) {
  const response = await apiClient.get('/booking-availability/', {
    params: { date },
  });

  return response.data;
}

export async function createBooking(bookingData) {
  const response = await apiClient.post('/bookings/', bookingData);
  return response.data;
}
