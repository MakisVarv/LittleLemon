import { useEffect, useState } from 'react';
import { getOrders, updateOrderStatus } from '../services/orders';

const DeliveryDashboardPage = () => {
  const [orders, setOrders] = useState([]);
  const [error, setError] = useState('');
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    async function loadOrders() {
      try {
        setIsLoading(true);
        setError('');

        const data = await getOrders();
        setOrders(data.results ?? data);
      } catch {
        setError('Could not load assigned orders.');
      } finally {
        setIsLoading(false);
      }
    }

    loadOrders();
  }, []);
  async function handleMarkDelivered(orderId) {
    try {
      setError('');

      await updateOrderStatus(orderId, 1);

      setOrders((prevOrders) =>
        prevOrders.map((order) =>
          order.id === orderId ? { ...order, status: true } : order,
        ),
      );
    } catch {
      setError('Could not update delivery status.');
    }
  }

  return (
    <main className="delivery-page">
      <h1>Delivery Dashboard</h1>
      <h2>Assigned Orders</h2>

      {isLoading && <p>Loading assigned orders...</p>}
      {error && <p className="error">{error}</p>}

      {!isLoading && !error && orders.length === 0 && (
        <p>No assigned orders yet.</p>
      )}

      {!isLoading && !error && orders.length > 0 && (
        <section className="delivery-list">
          {orders.map((order) => (
            <article key={order.id} className="delivery-order">
              <div className="delivery-order-header">
                <h3>Order #{order.id}</h3>

                <span
                  className={
                    order.status
                      ? 'status delivered'
                      : 'status pending'
                  }
                >
                  {order.status ? 'Delivered' : 'Pending'}
                </span>
              </div>

              <div className="delivery-order-meta">
                <p>
                  <strong>Total:</strong> ${order.total}
                </p>
                <p>
                  <strong>Date:</strong>{' '}
                  {new Date(order.date).toLocaleDateString()}
                </p>
              </div>

              <div className="delivery-items">
                <h4>Items</h4>

                {order.order_items.map((item) => (
                  <p key={item.id}>
                    {item.menuitem.title} × {item.quantity}
                  </p>
                ))}
              </div>

              {!order.status && (
                <button
                  type="button"
                  className="delivery-complete-btn"
                  onClick={() => handleMarkDelivered(order.id)}
                >
                  Mark as Delivered
                </button>
              )}
            </article>
          ))}
        </section>
      )}
    </main>
  );
};

export default DeliveryDashboardPage;
