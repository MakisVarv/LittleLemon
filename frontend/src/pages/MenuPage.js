import { useEffect, useState } from 'react';
import { getMenuItems } from '../services/menu';
import { addToCart } from '../services/cart';

const MenuPage = () => {
  const [menuItems, setMenuItems] = useState([]);
  const [error, setError] = useState('');
  const [isLoading, setIsLoading] = useState(true);
  const [cartMessage, setCartMessage] = useState('');
  const [addingItemId, setAddingItemId] = useState(null);
  useEffect(() => {
    async function loadMenuItems() {
      try {
        setIsLoading(true);
        setError('');

        const data = await getMenuItems();
        setMenuItems(data);
      } catch {
        setError('Could not load menu items.');
      } finally {
        setIsLoading(false);
      }
    }

    loadMenuItems();
  }, []);
  async function handleAddToCart(itemId) {
    try {
      setCartMessage('');
      setAddingItemId(itemId);

      await addToCart(itemId, 1);

      setCartMessage('Item added to cart.');
    } catch {
      setCartMessage(
        'Please log in as a customer to add items to cart.',
      );
    } finally {
      setAddingItemId(null);
    }
  }
  return (
    <main className="menu-page">
      <h1>Our Menu</h1>
      {cartMessage && <p className="cart-message">{cartMessage}</p>}
      {isLoading && <p>Loading menu...</p>}

      {error && <p className="error">{error}</p>}

      {!isLoading &&
        !error &&
        (menuItems.length === 0 ? (
          <p>No menu items available yet.</p>
        ) : (
          <section className="menu-grid">
            {menuItems.map((item) => (
              <article key={item.id} className="menu-card">
                <h2>{item.title}</h2>
                <p>{item.description}</p>
                <p className="menu-price">${item.price}</p>
                <button
                  type="button"
                  onClick={() => handleAddToCart(item.id)}
                  disabled={addingItemId === item.id}
                >
                  {addingItemId === item.id
                    ? 'Adding...'
                    : 'Add to cart'}
                </button>
              </article>
            ))}
          </section>
        ))}
    </main>
  );
};

export default MenuPage;
