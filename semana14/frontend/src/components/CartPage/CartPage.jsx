import { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';

import { useAuth } from '../../context/AuthContext';
import { useCart } from '../../context/CartContext';
import { createOrder } from '../../services/orderService';
import './CartPage.css';

const getApiErrorMessage = (requestError) => {
  const data = requestError.response?.data;

  if (typeof data?.detail === 'string') {
    return data.detail;
  }
  if (typeof data?.items === 'string') {
    return data.items;
  }
  if (Array.isArray(data?.items)) {
    return data.items.join(' ');
  }

  return 'Unable to place the order. Please try again.';
};

function CartPage() {
  const { isAuthenticated } = useAuth();
  const {
    items,
    updateQuantity,
    removeFromCart,
    clearCart,
    totalItems,
    provisionalTotal,
  } = useCart();
  const navigate = useNavigate();
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [error, setError] = useState('');

  const handleCheckout = async () => {
    if (!isAuthenticated) {
      navigate('/login', { state: { from: '/cart' } });
      return;
    }

    setIsSubmitting(true);
    setError('');

    try {
      const response = await createOrder(
        items.map((item) => ({
          product_id: item.id,
          quantity: item.quantity,
        })),
      );

      if (response.status === 201) {
        clearCart();
        navigate('/my-orders', {
          state: {
            confirmation: {
              id: response.data.id,
              total: response.data.total,
              status: response.data.status,
            },
          },
        });
      }
    } catch (requestError) {
      setError(getApiErrorMessage(requestError));
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <section className="cart-page">
      <h1>Shopping Cart</h1>

      {error && (
        <p className="cart-error" role="alert">
          {error}
        </p>
      )}

      {items.length === 0 ? (
        <div className="cart-empty">
          <p>Your cart is empty.</p>
          <Link to="/">Back to products</Link>
        </div>
      ) : (
        <>
          <ul className="cart-items">
            {items.map((item) => (
              <li className="cart-item" key={item.id}>
                {item.image ? (
                  <img
                    className="cart-item-image"
                    src={item.image}
                    alt={item.name}
                  />
                ) : (
                  <div className="cart-item-placeholder">No image available</div>
                )}

                <div className="cart-item-details">
                  <h2>{item.name}</h2>
                  <p>Unit price: ${Number(item.price).toFixed(2)}</p>
                  <div className="quantity-controls">
                    <button
                      type="button"
                      onClick={() =>
                        updateQuantity(item.id, item.quantity - 1)
                      }
                      disabled={item.quantity <= 1}
                      aria-label={`Decrease quantity of ${item.name}`}
                    >
                      -
                    </button>
                    <span>{item.quantity}</span>
                    <button
                      type="button"
                      onClick={() =>
                        updateQuantity(item.id, item.quantity + 1)
                      }
                      aria-label={`Increase quantity of ${item.name}`}
                    >
                      +
                    </button>
                  </div>
                  <button
                    className="remove-button"
                    type="button"
                    onClick={() => removeFromCart(item.id)}
                  >
                    Remove
                  </button>
                </div>

                <p className="cart-item-total">
                  ${(Number(item.price) * item.quantity).toFixed(2)}
                </p>
              </li>
            ))}
          </ul>

          <div className="cart-summary">
            <p>Items: {totalItems}</p>
            <p className="cart-total">
              Provisional total: ${provisionalTotal.toFixed(2)}
            </p>
            <p className="provisional-note">
              This amount is provisional until it is confirmed and validated
              by the server.
            </p>
            <button
              className="checkout-button"
              type="button"
              onClick={handleCheckout}
              disabled={isSubmitting}
            >
              {isSubmitting ? 'Placing order...' : 'Place Order'}
            </button>
          </div>
        </>
      )}
    </section>
  );
}

export default CartPage;
