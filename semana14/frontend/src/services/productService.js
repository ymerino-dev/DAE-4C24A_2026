import api from './api';

const MULTIPART_HEADERS = {
  'Content-Type': 'multipart/form-data',
};

export const getProducts = async (categoryId = null) => {
  const url = categoryId
    ? `/products/?category=${categoryId}`
    : '/products/';
  return api.get(url);
};

export const getProductById = async (id) =>
  api.get(`/products/${id}/`);

export const createProduct = async (formData) =>
  api.post('/products/', formData, {
    headers: MULTIPART_HEADERS,
  });

export const updateProduct = async (id, formData) =>
  api.patch(`/products/${id}/`, formData, {
    headers: MULTIPART_HEADERS,
  });

export const deleteProduct = async (id) =>
  api.delete(`/products/${id}/`);
