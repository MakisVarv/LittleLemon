import React from 'react';
import GreekSalad from '../assets/greek-salad.jpg';
import Bruschetta from '../assets/bruschetta.jpg';
import LemonDessert from '../assets/lemon-dessert.jpg';
import { Link } from 'react-router-dom';

const Specials = () => {
  return (
    <section className="specials">
      <header className="specials-header">
        <h2>Specials</h2>
        <Link className="btn-primary" to="/menu">
          Online Menu
        </Link>
      </header>

      <section className="cards">
        <article className="card">
          <img src={GreekSalad} alt="Greek Salad" />
          <h3>
            Greek Salad <span>$12.99</span>
          </h3>
          <p>
            The famous greek salad of crispy lettuce, peppers, olives
            and our Chicago style feta cheese, garnished with crunchy
            garlic and rosemary croutons.
          </p>
          <a href="#">Order a delivery 🚚</a>
        </article>

        <article className="card">
          <img src={Bruschetta} alt="Bruschetta" />
          <h3>
            Bruschetta <span>$5.99</span>
          </h3>
          <p>
            Our Bruschetta is made from grilled bread that has been
            smeared with garlic and seasoned with salt and olive oil.
          </p>
          <a href="#">Order a delivery 🚚</a>
        </article>

        <article className="card">
          <img src={LemonDessert} alt="Lemon Dessert" />
          <h3>
            Lemon Dessert <span>$5.00</span>
          </h3>
          <p>
            This comes straight from grandma’s recipe book, every last
            ingredient has been sourced and is as authentic as can be
            imagined.
          </p>
          <a href="#">Order a delivery 🚚</a>
        </article>
      </section>
    </section>
  );
};

export default Specials;
