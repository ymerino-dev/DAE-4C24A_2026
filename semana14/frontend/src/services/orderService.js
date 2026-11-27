import api from './api';

export const createOrder = async (items) => api.post('/orders/', { items });
