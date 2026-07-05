import { useEffect, useState } from 'react';
import { getCartItems } from '../services/cart';
import { createOrder } from '../services/orders';

const CartPage = () => {
  const [cartItems, setCartItems] = useState([]);
  const [error, setError] = useState('');
  const [isLoading, setIsLoading] = useState(true);
  const [orderMessage, setOrderMessage] = useState('');
  const [isOrdering, setIsOrdering] = useState(false);

  useEffect(() => {
    async function loadCartItems() {
      try {
        setIsLoading(true);
        setError('');

        const data = await getCartItems();
        setCartItems(data);
      } catch {
        setError('Could not load cart.');
      } finally {
        setIsLoading(false);
      }
    }

    loadCartItems();
  }, []);
  async function handlePlaceOrder() {
    try {
      setIsOrdering(true);
      setError('');
      setOrderMessage('');

      await createOrder();
      setCartItems([]);
      setOrderMessage('Order placed successfully.');
    } catch {
      setError('Could not place order.');
    } finally {
      setIsOrdering(false);
    }
  }
  const cartTotal = cartItems.reduce(
    (total, item) => total + Number(item.price),
    0,
  );
  return (
    <main className="cart-page">
      <h1>Your Cart</h1>

      {isLoading && <p>Loading cart...</p>}

      {error && <p className="error">{error}</p>}
      {orderMessage && <p className="success">{orderMessage}</p>}
      {!isLoading && !error && cartItems.length === 0 && (
        <p>Your cart is empty.</p>
      )}

      {!isLoading && !error && cartItems.length > 0 && (
        <section className="cart-list">
          {cartItems.map((item) => (
            <article key={item.id} className="cart-item">
              <h2>{item.menuitem.title}</h2>
              <p>Quantity: {item.quantity}</p>
              <p>Unit price: ${item.unit_price}</p>
              <p>Total: ${item.price}</p>
            </article>
          ))}
          <p className="cart-total">
            Cart total: ${cartTotal.toFixed(2)}
          </p>
          <button
            type="button"
            onClick={handlePlaceOrder}
            disabled={isOrdering}
          >
            {isOrdering ? 'Placing order...' : 'Place order'}
          </button>
        </section>
      )}
    </main>
  );
};

export default CartPage;
