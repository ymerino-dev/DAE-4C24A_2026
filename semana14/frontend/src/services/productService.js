import apiClient from './apiClient';

const MULTIPART_HEADERS = {
  'Content-Type': 'multipart/form-data',
};

export const getProducts = async (categoryId = null) => {
  const url = categoryId
    ? `/products/?category=${categoryId}`
    : '/products/';
  return apiClient.get(url);
};

export const getProductById = async (id) =>
  apiClient.get(`/products/${id}/`);

export const createProduct = async (formData) =>
  apiClient.post('/products/', formData, {
    headers: MULTIPART_HEADERS,
  });

export const updateProduct = async (id, formData) =>
  apiClient.patch(`/products/${id}/`, formData, {
    headers: MULTIPART_HEADERS,
  });

export const deleteProduct = async (id) =>
  apiClient.delete(`/products/${id}/`);
