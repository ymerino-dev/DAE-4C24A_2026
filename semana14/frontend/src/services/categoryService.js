import api from './api';

export const getCategories = async () => api.get('/categories/');

export const getCategoryById = async (id) => api.get(`/categories/${id}/`);

export const createCategory = async (data) =>
  api.post('/categories/', data);

export const updateCategory = async (id, data) =>
  api.put(`/categories/${id}/`, data);

export const deleteCategory = async (id) => api.delete(`/categories/${id}/`);
