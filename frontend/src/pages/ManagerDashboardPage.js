import { useEffect, useState } from 'react';
import { getDeliveryCrewUsers } from '../services/users';
import {
  getOrders,
  updateOrderStatus,
  assignDeliveryCrew,
} from '../services/orders';

const ManagerDashboardPage = () => {
  const [orders, setOrders] = useState([]);
  const [error, setError] = useState('');
  const [deliveryCrew, setDeliveryCrew] = useState([]);
  const [isLoading, setIsLoading] = useState(true);
  useEffect(() => {
    async function loadOrders() {
      try {
        setIsLoading(true);
        setError('');
        const ordersData = await getOrders();
        const deliveryData = await getDeliveryCrewUsers();
        setOrders(ordersData.results ?? ordersData);
        setDeliveryCrew(deliveryData);
      } catch {
        setError('Could not fetch orders');
      } finally {
        setIsLoading(false);
      }
    }

    loadOrders();
  }, []);

  async function handleAssignDelivery(orderId, deliveryCrewId) {
    if (!deliveryCrewId) return;

    try {
      setError('');

      await assignDeliveryCrew(orderId, Number(deliveryCrewId));

      setOrders((prevOrders) =>
        prevOrders.map((order) =>
          order.id === orderId
            ? { ...order, delivery_crew: Number(deliveryCrewId) }
            : order,
        ),
      );
    } catch {
      setError('Could not assign delivery crew.');
    }
  }
  async function handleToggleStatus(order) {
    try {
      setError('');

      const nextStatus = order.status ? 0 : 1;

      await updateOrderStatus(order.id, nextStatus);

      setOrders((prevOrders) =>
        prevOrders.map((currentOrder) =>
          currentOrder.id === order.id
            ? { ...currentOrder, status: !currentOrder.status }
            : currentOrder,
        ),
      );
    } catch {
      setError('Could not update order status.');
    }
  }
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
                <th>Delivery Crew</th>
              </tr>
            </thead>

            <tbody>
              {orders.map((order) => (
                <tr key={order.id}>
                  <td>#{order.id}</td>
                  <td>{order.user}</td>
                  <td>
                    <span
                      className={
                        order.status
                          ? 'status delivered'
                          : 'status pending'
                      }
                    >
                      {order.status ? 'Delivered' : 'Pending'}
                    </span>

                    <button
                      type="button"
                      className="status-toggle-btn"
                      onClick={() => handleToggleStatus(order)}
                    >
                      Mark as {order.status ? 'Pending' : 'Delivered'}
                    </button>
                  </td>
                  <td>${order.total}</td>
                  <td>{new Date(order.date).toLocaleDateString()}</td>
                  <td>
                    {order.order_items.map((item) => (
                      <div key={item.id}>
                        {item.menuitem.title} × {item.quantity}
                      </div>
                    ))}
                  </td>
                  <td>
                    <select
                      className="delivery-select"
                      value={order.delivery_crew ?? ''}
                      onChange={(e) =>
                        handleAssignDelivery(order.id, e.target.value)
                      }
                    >
                      <option value="">Unassigned</option>

                      {deliveryCrew.map((user) => (
                        <option key={user.id} value={user.id}>
                          {user.username}
                        </option>
                      ))}
                    </select>
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
