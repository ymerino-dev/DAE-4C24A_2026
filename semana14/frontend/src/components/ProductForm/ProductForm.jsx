import { useCallback, useEffect, useState } from 'react';
import { useNavigate, useParams } from 'react-router-dom';

import { getCategories } from '../../services/categoryService';
import {
  createProduct,
  getProductById,
  updateProduct,
} from '../../services/productService';
import './ProductForm.css';

const INITIAL_FORM_DATA = {
  name: '',
  description: '',
  price: '',
  stock: '0',
  category_id: '',
};

const toFormData = (product) => ({
  name: product.name ?? '',
  description: product.description ?? '',
  price: product.price ?? '',
  stock: String(product.stock ?? 0),
  category_id: String(product.category?.id ?? ''),
});

function ProductForm() {
  const { id } = useParams();
  const navigate = useNavigate();
  const isEditMode = Boolean(id);

  const [categories, setCategories] = useState([]);
  const [formData, setFormData] = useState(INITIAL_FORM_DATA);
  const [selectedFile, setSelectedFile] = useState(null);
  const [isLoading, setIsLoading] = useState(isEditMode);
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [serverErrors, setServerErrors] = useState({});
  const [submitError, setSubmitError] = useState(null);

  const fetchCategories = useCallback(async () => {
    const response = await getCategories();
    return response.data;
  }, []);

  const fetchProduct = useCallback(async (productId) => {
    const response = await getProductById(productId);
    return response.data;
  }, []);

  useEffect(() => {
    const requests = [fetchCategories()];
    if (id) {
      requests.push(fetchProduct(id));
    }

    Promise.all(requests)
      .then((results) => {
        setCategories(results[0]);
        if (id) {
          setFormData(toFormData(results[1]));
        }
      })
      .catch((requestError) => setSubmitError(requestError))
      .finally(() => setIsLoading(false));
  }, [fetchCategories, fetchProduct, id]);

  const handleChange = (event) => {
    const { name, value } = event.target;
    setFormData((currentData) => ({
      ...currentData,
      [name]: value,
    }));
  };

  const handleFileChange = (event) => {
    setSelectedFile(event.target.files?.[0] ?? null);
  };

  const handleSubmit = async (event) => {
    event.preventDefault();
    setServerErrors({});
    setSubmitError(null);
    setIsSubmitting(true);

    const payload = new FormData();
    payload.append('name', formData.name);
    payload.append('description', formData.description);
    payload.append('price', formData.price);
    payload.append('stock', formData.stock);
    payload.append('category_id', formData.category_id);

    if (selectedFile) {
      payload.append('image', selectedFile);
    }

    try {
      if (isEditMode) {
        await updateProduct(id, payload);
      } else {
        await createProduct(payload);
      }
      navigate('/');
    } catch (requestError) {
      if (requestError.response?.status === 400) {
        const errorData = requestError.response.data;
        setServerErrors(
          errorData && typeof errorData === 'object' ? errorData : {},
        );
      } else {
        setSubmitError(requestError);
      }
    } finally {
      setIsSubmitting(false);
    }
  };

  const renderFieldError = (fieldName) => {
    const messages = serverErrors[fieldName];
    if (!messages) {
      return null;
    }

    const messageList = Array.isArray(messages) ? messages : [messages];

    return (
      <div className="field-error" role="alert">
        {messageList.map((message, index) => (
          <p key={`${fieldName}-${index}`}>{message}</p>
        ))}
      </div>
    );
  };

  if (isLoading) {
    return (
      <section className="product-form-container">
        <p className="loading-text">Loading product...</p>
      </section>
    );
  }

  return (
    <section className="product-form-container">
      <h1>{isEditMode ? 'Edit Product' : 'Create Product'}</h1>
      <p className="form-subtitle">
        {isEditMode
          ? 'Update the product details below.'
          : 'Add a new product to the catalog.'}
      </p>

      {submitError !== null && (
        <div className="form-error" role="alert">
          {submitError.message}
        </div>
      )}

      <form onSubmit={handleSubmit} noValidate>
        <div className="form-field">
          <label htmlFor="name">Name</label>
          <input
            id="name"
            name="name"
            type="text"
            value={formData.name}
            onChange={handleChange}
          />
          {renderFieldError('name')}
        </div>

        <div className="form-field">
          <label htmlFor="description">Description</label>
          <textarea
            id="description"
            name="description"
            rows="4"
            value={formData.description}
            onChange={handleChange}
          />
          {renderFieldError('description')}
        </div>

        <div className="form-row">
          <div className="form-field">
            <label htmlFor="price">Price</label>
            <input
              id="price"
              name="price"
              type="number"
              step="0.01"
              value={formData.price}
              onChange={handleChange}
            />
            {renderFieldError('price')}
          </div>

          <div className="form-field">
            <label htmlFor="stock">Stock</label>
            <input
              id="stock"
              name="stock"
              type="number"
              step="1"
              value={formData.stock}
              onChange={handleChange}
            />
            {renderFieldError('stock')}
          </div>
        </div>

        <div className="form-field">
          <label htmlFor="category_id">Category</label>
          <select
            id="category_id"
            name="category_id"
            value={formData.category_id}
            onChange={handleChange}
          >
            <option value="">Select a category</option>
            {categories.map((category) => (
              <option key={category.id} value={category.id}>
                {category.name}
              </option>
            ))}
          </select>
          {renderFieldError('category_id')}
          {renderFieldError('category')}
        </div>

        <div className="form-field">
          <label htmlFor="image">Image</label>
          <input
            id="image"
            name="image"
            type="file"
            accept="image/*"
            onChange={handleFileChange}
          />
          {isEditMode && (
            <p className="field-hint">
              Leave empty to keep the current image.
            </p>
          )}
          {renderFieldError('image')}
        </div>

        <button className="submit-button" type="submit" disabled={isSubmitting}>
          {isSubmitting
            ? 'Saving...'
            : isEditMode
              ? 'Save Changes'
              : 'Create Product'}
        </button>
      </form>
    </section>
  );
}

export default ProductForm;
