import { useEffect, useState } from 'react';
import { getCartItems } from '../services/cart';

const CartPage = () => {
  const [cartItems, setCartItems] = useState([]);
  const [error, setError] = useState('');
  const [isLoading, setIsLoading] = useState(true);

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

  return (
    <main className="cart-page">
      <h1>Your Cart</h1>

      {isLoading && <p>Loading cart...</p>}

      {error && <p className="error">{error}</p>}

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
        </section>
      )}
    </main>
  );
};

export default CartPage;
