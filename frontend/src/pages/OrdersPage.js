import { useEffect, useState } from 'react';
import { getOrders } from '../services/orders';

const OrdersPage = () => {
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
        setError('Could not load orders.');
      } finally {
        setIsLoading(false);
      }
    }
    loadOrders();
  }, []);

  return (
    <main className="order-page">
      <h1>Your Orders</h1>

      {isLoading && <p>Loading orders...</p>}

      {error && <p className="error">{error}</p>}
      {!isLoading && !error && orders.length === 0 && (
        <p>You have not placed any orders</p>
      )}

      {!isLoading && !error && orders.length > 0 && (
        <section className="order-list">
          {orders.map((order) => (
            <article key={order.id} className="order">
              <h2>Order # {order.id}</h2>
              <p>Status : {order.status ? 'Delivered' : 'Pending'}</p>
              <div>
                {order.order_items.map((item) => (
                  <section key={item.id} className="order-item">
                    <h2>{item.menuitem.title}</h2>
                    <p>Quantity: {item.quantity}</p>
                    <p>Price: ${item.price}</p>
                  </section>
                ))}
              </div>
              <p>Total: ${order.total}</p>
              <p>Date: {new Date(order.date).toLocaleDateString()}</p>
            </article>
          ))}
        </section>
      )}
    </main>
  );
};

export default OrdersPage;
