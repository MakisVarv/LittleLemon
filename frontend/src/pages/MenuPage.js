import { useEffect, useState } from 'react';
import { getMenuItems } from '../services/menu';

const MenuPage = () => {
  const [menuItems, setMenuItems] = useState([]);
  const [error, setError] = useState('');
  const [isLoading, setIsLoading] = useState(true);
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
  return (
    <main className="menu-page">
      <h1>Our Menu</h1>
      {isLoading && <p>Loading menu...</p>}

      {error && <p className="error">{error}</p>}

      {!isLoading && !error && (
        <section className="menu-grid">
          {menuItems.map((item) => (
            <article key={item.id} className="menu-card">
              <h2>{item.title}</h2>
              <p>{item.description}</p>
              <p>${item.price}</p>
            </article>
          ))}
        </section>
      )}
    </main>
  );
};

export default MenuPage;
