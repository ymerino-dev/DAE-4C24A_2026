import { useEffect, useState } from 'react';
import { Link, useNavigate, useParams } from 'react-router-dom';

import { useCart } from '../../context/CartContext';
import { getProductById } from '../../services/productService';
import './ProductDetailPage.css';

function ProductDetailPage() {
  const { id } = useParams();
  const navigate = useNavigate();
  const { addToCart } = useCart();
  const [request, setRequest] = useState({
    id: null,
    product: null,
    error: '',
  });

  const isLoading = request.id !== id;
  const { product, error } = request;

  useEffect(() => {
    let isActive = true;

    getProductById(id)
      .then((response) => {
        if (isActive) {
          setRequest({ id, product: response.data, error: '' });
        }
      })
      .catch((requestError) => {
        if (isActive) {
          const detail = requestError.response?.data?.detail;
          setRequest({
            id,
            product: null,
            error:
              typeof detail === 'string'
                ? detail
                : 'Unable to load the product. Please try again.',
          });
        }
      });

    return () => {
      isActive = false;
    };
  }, [id]);

  if (isLoading) {
    return <p className="product-detail-message">Loading product...</p>;
  }

  if (error) {
    return (
      <div className="product-detail-error" role="alert">
        <h1>Unable to load the product</h1>
        <p>{error}</p>
        <Link to="/">Back to catalog</Link>
      </div>
    );
  }

  return (
    <article className="product-detail">
      <Link className="product-detail-back" to="/">
        Back to catalog
      </Link>

      <div className="product-detail-grid">
        {product.image ? (
          <img
            className="product-detail-image"
            src={product.image}
            alt={product.name}
          />
        ) : (
          <div className="product-detail-placeholder">No image available</div>
        )}

        <div className="product-detail-info">
          <span className="product-detail-category">
            {product.category?.name}
          </span>
          <h1>{product.name}</h1>
          <p className="product-detail-description">{product.description}</p>
          <p className="product-detail-price">${product.price}</p>
          <p className="product-detail-stock">Stock: {product.stock}</p>

          <div className="product-detail-actions">
            <button
              className="product-detail-cart-button"
              type="button"
              onClick={() => addToCart(product, 1)}
              disabled={product.stock <= 0}
            >
              Add to Cart
            </button>
            <button
              className="product-detail-secondary"
              type="button"
              onClick={() => navigate('/cart')}
            >
              Go to Cart
            </button>
          </div>
        </div>
      </div>
    </article>
  );
}

export default ProductDetailPage;
