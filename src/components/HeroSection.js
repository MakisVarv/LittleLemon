import React from "react";
import { useNavigate } from "react-router-dom";

const HeroSection = () => {

  const navigate = useNavigate();

  const handleReserveClick = () => {
    navigate("/booking"); // <-- redirect path
  };

  return (
    <main className="hero">
      <article className="hero-text">
        <h1>Little Lemon</h1>
        <h3>Chicago</h3>
        <p>
          Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do
          eiusmod tempor incididunt ut labore et dolore magna aliqua.
        </p>
        <button onClick={handleReserveClick}>Reserve a Table</button>
      </article>
      <img src="#" alt="Hero Image" />
    </main>
  );
};

export default HeroSection;
