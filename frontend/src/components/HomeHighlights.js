import Grill from '../assets/Grill.jpg';
import salad from '../assets/salad.jpg';
import head_chef from '../assets/head_chef.jpg';
import { Link } from 'react-router-dom';
const HomeHighlights = () => {
  return (
    <section className="home-highlights">
      <article className="highlight-card">
        <h2>Our New Menu</h2>
        <img src={Grill} alt="Grilled Mediterranean skewers" />
        <p>
          Our menu consists of 12-15 seasonal items based on Italian,
          Greek, and Turkish culture.
        </p>
        <p>
          <Link to="/menu">See our new menu</Link>
        </p>
      </article>
      <article className="highlight-card">
        <h2>Book a table</h2>
        <img src={salad} alt="salad" />
        <p>
          Reserve your table for an Italian, Greek, and Turkish dining
          experience.
        </p>
        <p>
          <Link className="text-link" to="/booking">
            Book your table now
          </Link>
        </p>
      </article>
      <article className="highlight-card">
        <h2>Opening Hours</h2>
        <img src={head_chef} alt="chef" />
        <p>
          The Little Lemon Restaurant is open 7 days a week, except
          for public holidays.
        </p>
        <ul>
          <li>Mon - Fri: 2pm - 10pm</li>
          <li>Sat: 2pm - 11pm</li>
          <li>Sun: 2pm - 9pm</li>
        </ul>
      </article>
    </section>
  );
};
export default HomeHighlights;
