import apiClient from './apiClient';

export const getCategories = async () => apiClient.get('/categories/');

export const getCategoryById = async (id) =>
  apiClient.get(`/categories/${id}/`);

export const createCategory = async (data) =>
  apiClient.post('/categories/', data);

export const updateCategory = async (id, data) =>
  apiClient.put(`/categories/${id}/`, data);

export const deleteCategory = async (id) =>
  apiClient.delete(`/categories/${id}/`);
