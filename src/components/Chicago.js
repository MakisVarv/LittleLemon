import React from "react";

const Chicago = () => {
  return (
    <section className="chicago">
      <article className="chicago-text">
        <h2>Little Lemon</h2>
        <h3>Chicago</h3>
        <p>
          Little Lemon is a charming neighborhood bistro that serves simple food
          and classic cocktails in a lively but casual environment. The chefs
          draw inspiration from Italian, Greek, and Turkish culture and have a
          menu of 12–15 items that they rotate seasonally.
        </p>
        <p>
          The restaurant has a rustic and relaxed atmosphere with moderate
          prices, making it a popular place for a meal any time of the day.
        </p>
      </article>

      <aside className="chicago-images">
        <img src="#" alt="Restaurant Interior" className="image-top" />
        <img src="#" alt="Chefs in Kitchen" className="image-bottom" />
      </aside>
    </section>
  );
};

export default Chicago;
