import { useCallback, useEffect, useState } from 'react';
import { Link, useLocation } from 'react-router-dom';

import { getMyOrders } from '../../services/orderService';
import './MyOrdersPage.css';

const formatDate = (value) => {
  const date = new Date(value);
  return Number.isNaN(date.getTime()) ? value : date.toLocaleString();
};

const getProductLabel = (item) =>
  item.product_name || item.product?.name || `Product #${item.product}`;

function MyOrdersPage() {
  const location = useLocation();
  const confirmation = location.state?.confirmation;
  const [orders, setOrders] = useState([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState('');

  const fetchOrders = useCallback(async () => {
    try {
      const response = await getMyOrders();
      setOrders(response.data);
      setError('');
    } catch (requestError) {
      const detail = requestError.response?.data?.detail;
      setError(
        typeof detail === 'string'
          ? detail
          : 'Unable to load orders. Please try again.',
      );
    } finally {
      setIsLoading(false);
    }
  }, []);

  const handleRetry = () => {
    setIsLoading(true);
    setError('');
    fetchOrders();
  };

  useEffect(() => {
    let isActive = true;

    getMyOrders()
      .then((response) => {
        if (isActive) {
          setOrders(response.data);
          setError('');
        }
      })
      .catch((requestError) => {
        if (isActive) {
          const detail = requestError.response?.data?.detail;
          setError(
            typeof detail === 'string'
              ? detail
              : 'Unable to load orders. Please try again.',
          );
        }
      })
      .finally(() => {
        if (isActive) {
          setIsLoading(false);
        }
      });

    return () => {
      isActive = false;
    };
  }, []);

  return (
    <section className="my-orders-page">
      <div className="my-orders-header">
        <h1>My Orders</h1>
        <Link to="/">Continue shopping</Link>
      </div>

      {confirmation && (
        <p className="order-confirmation" role="status">
          Order #{confirmation.id} placed successfully. Confirmed total: $
          {Number(confirmation.total).toFixed(2)}.
        </p>
      )}

      {isLoading ? (
        <p className="orders-loading">Loading orders...</p>
      ) : error ? (
        <div className="orders-error" role="alert">
          <p>{error}</p>
          <button type="button" onClick={handleRetry}>
            Retry
          </button>
        </div>
      ) : orders.length === 0 ? (
        <p className="orders-empty">You have no orders yet.</p>
      ) : (
        <ul className="orders-list">
          {orders.map((order) => (
            <li className="order-card" key={order.id}>
              <div className="order-heading">
                <h2>Order #{order.id}</h2>
                <span
                  className={`order-status status-${order.status.toLowerCase()}`}
                >
                  {order.status}
                </span>
              </div>

              <div className="order-meta">
                <span>Placed: {formatDate(order.created_at)}</span>
                <span className="order-total">
                  Confirmed total: ${Number(order.total).toFixed(2)}
                </span>
              </div>

              <h3>Products</h3>
              <ul className="order-items">
                {(order.items ?? []).map((item) => (
                  <li key={item.id}>
                    <span>{getProductLabel(item)}</span>
                    <span>
                      {item.quantity} x ${Number(item.unit_price).toFixed(2)}
                    </span>
                    <strong>
                      ${(Number(item.unit_price) * item.quantity).toFixed(2)}
                    </strong>
                  </li>
                ))}
              </ul>
            </li>
          ))}
        </ul>
      )}
    </section>
  );
}

export default MyOrdersPage;
