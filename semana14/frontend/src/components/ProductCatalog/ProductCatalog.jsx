import { useCallback, useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';

import { getCategories } from '../../services/categoryService';
import { deleteProduct, getProducts } from '../../services/productService';
import './ProductCatalog.css';

const SKELETON_CARDS = [1, 2, 3, 4, 5, 6];

function ProductCatalog() {
  const navigate = useNavigate();
  const [products, setProducts] = useState([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState(null);
  const [categories, setCategories] = useState([]);
  const [selectedCategory, setSelectedCategory] = useState(null);

  const fetchCatalogData = useCallback(async (categoryId) => {
    const [categoryResponse, productResponse] = await Promise.all([
      getCategories(),
      getProducts(categoryId),
    ]);

    return {
      categories: categoryResponse.data,
      products: productResponse.data,
    };
  }, []);

  const applyCatalogData = useCallback((catalogData) => {
    setCategories(catalogData.categories);
    setProducts(catalogData.products);
    setError(null);
    setIsLoading(false);
  }, []);

  const handleFetchError = useCallback((requestError) => {
    setError(requestError);
    setIsLoading(false);
  }, []);

  useEffect(() => {
    fetchCatalogData(selectedCategory)
      .then(applyCatalogData)
      .catch(handleFetchError);
  }, [applyCatalogData, fetchCatalogData, handleFetchError, selectedCategory]);

  const handleCategoryChange = (event) => {
    setSelectedCategory(event.target.value || null);
    setIsLoading(true);
    setError(null);
  };

  const handleRetry = () => {
    setIsLoading(true);
    setError(null);
    fetchCatalogData(selectedCategory)
      .then(applyCatalogData)
      .catch(handleFetchError);
  };

  const handleDelete = async (id) => {
    try {
      await deleteProduct(id);
      setProducts((currentProducts) =>
        currentProducts.filter((product) => product.id !== id),
      );
    } catch (requestError) {
      setError(requestError);
    }
  };

  const errorDetails = error
    ? error.response
      ? `${error.message} - ${JSON.stringify(error.response.data)}`
      : error.message
    : '';

  return (
    <section className="catalog" aria-busy={isLoading}>
      <div className="catalog-header">
        <h1>Product Catalog</h1>
        <label className="category-filter">
          Category
          <select
            value={selectedCategory ?? ''}
            onChange={handleCategoryChange}
          >
            <option value="">All Categories</option>
            {categories.map((category) => (
              <option key={category.id} value={category.id}>
                {category.name}
              </option>
            ))}
          </select>
        </label>
      </div>

      {isLoading ? (
        <div>
          <p className="loading-text">Loading catalog...</p>
          <div className="product-grid">
            {SKELETON_CARDS.map((cardId) => (
              <article className="product-card skeleton-card" key={cardId}>
                <div className="skeleton-bar skeleton-image" />
                <div className="product-body">
                  <div className="skeleton-bar skeleton-line short" />
                  <div className="skeleton-bar skeleton-line" />
                  <div className="skeleton-bar skeleton-line" />
                  <div className="skeleton-bar skeleton-line short" />
                </div>
              </article>
            ))}
          </div>
        </div>
      ) : error !== null ? (
        <div className="error-box" role="alert">
          <h2>Unable to load the catalog</h2>
          <p className="error-details">{errorDetails}</p>
          <button className="retry-button" type="button" onClick={handleRetry}>
            Retry
          </button>
        </div>
      ) : products.length === 0 ? (
        <p className="empty-message">No products found.</p>
      ) : (
        <div className="product-grid">
          {products.map((product) => (
            <article className="product-card" key={product.id}>
              {product.image ? (
                <img
                  className="product-image"
                  src={product.image}
                  alt={product.name}
                />
              ) : (
                <div className="product-image-placeholder">
                  No image available
                </div>
              )}
              <div className="product-body">
                <span className="product-category">
                  {product.category?.name}
                </span>
                <h2>{product.name}</h2>
                <p className="product-description">{product.description}</p>
                <div className="product-meta">
                  <span className="product-price">${product.price}</span>
                  <span className="product-stock">
                    Stock: {product.stock}
                  </span>
                </div>
                <div className="product-actions">
                  <button
                    className="edit-button"
                    type="button"
                    onClick={() => navigate(`/edit/${product.id}`)}
                  >
                    Edit
                  </button>
                  <button
                    className="delete-button"
                    type="button"
                    onClick={() => handleDelete(product.id)}
                  >
                    Delete
                  </button>
                </div>
              </div>
            </article>
          ))}
        </div>
      )}
    </section>
  );
}

export default ProductCatalog;
