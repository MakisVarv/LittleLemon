import { useEffect, useState } from 'react';
import { getOrders } from '../services/orders';

const ManagerDashboardPage = () => {
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
        setError('Could not fetch orders');
      } finally {
        setIsLoading(false);
      }
    }

    loadOrders();
  }, []);
  return (
    <main className="manager-page">
      <h1>Manager Dashboard</h1>
      <h2>Orders</h2>

      {isLoading && <p>Loading orders...</p>}
      {error && <p className="error">{error}</p>}

      {!isLoading && !error && orders.length === 0 && (
        <p>No orders found.</p>
      )}

      {!isLoading && !error && orders.length > 0 && (
        <div className="manager-table-wrapper">
          <table className="manager-table">
            <thead>
              <tr>
                <th>Order</th>
                <th>User</th>
                <th>Status</th>
                <th>Total</th>
                <th>Date</th>
                <th>Items</th>
              </tr>
            </thead>

            <tbody>
              {orders.map((order) => (
                <tr key={order.id}>
                  <td>#{order.id}</td>
                  <td>{order.user}</td>
                  <td>{order.status ? 'Delivered' : 'Pending'}</td>
                  <td>${order.total}</td>
                  <td>{new Date(order.date).toLocaleDateString()}</td>
                  <td>
                    {order.order_items.map((item) => (
                      <div key={item.id}>
                        {item.menuitem.title} × {item.quantity}
                      </div>
                    ))}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </main>
  );
};
export default ManagerDashboardPage;
