import { useState } from 'react';
import { Link } from 'react-router-dom';

import { useCart } from '../../context/CartContext';
import { createOrder } from '../../services/orderService';
import './CartPage.css';

function CartPage() {
  const {
    items,
    updateQuantity,
    removeFromCart,
    clearCart,
    totalItems,
    provisionalTotal,
  } = useCart();
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [error, setError] = useState('');
  const [confirmation, setConfirmation] = useState(null);

  const handleCheckout = async () => {
    setIsSubmitting(true);
    setError('');
    setConfirmation(null);

    try {
      const response = await createOrder(
        items.map((item) => ({
          product_id: item.id,
          quantity: item.quantity,
        })),
      );

      setConfirmation(response.data);
      clearCart();
    } catch (requestError) {
      const detail =
        requestError.response?.data?.detail ||
        requestError.response?.data?.items ||
        'Unable to place the order. Please try again.';
      setError(typeof detail === 'string' ? detail : JSON.stringify(detail));
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

      {confirmation && (
        <p className="cart-success" role="status">
          Order #{confirmation.id} placed with total $
          {Number(confirmation.total).toFixed(2)}.
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
                  <div className="cart-item-placeholder">
                    No image available
                  </div>
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
