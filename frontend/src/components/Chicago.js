import React from 'react';
import RestaurantImage from '../assets/restauranfood.jpg';
import ChefsInKitchen from '../assets/mario-adrian-b.jpg';

const Chicago = () => {
  return (
    <section className="chicago">
      <article className="chicago-text">
        <h2>Our Story</h2>
        <h3>Little Lemon-Chicago</h3>
        <p>
          Little Lemon is a charming neighborhood bistro that serves
          simple food and classic cocktails in a lively but casual
          environment. The chefs draw inspiration from Italian, Greek,
          and Turkish culture and have a menu of 12–15 items that they
          rotate seasonally.
        </p>
        <p>
          The restaurant has a rustic and relaxed atmosphere with
          moderate prices, making it a popular place for a meal any
          time of the day.
        </p>
      </article>

      <aside className="chicago-images">
        <img
          src={ChefsInKitchen}
          alt="Chefs in Kitchen"
          className="image-top"
        />
        <img
          src={RestaurantImage}
          alt="Restaurant Interior"
          className="image-bottom"
        />
      </aside>
    </section>
  );
};

export default Chicago;
