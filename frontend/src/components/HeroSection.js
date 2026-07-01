import React from 'react';
import { useNavigate } from 'react-router-dom';
import HeroImage from '../assets/restauranfood.jpg';

const HeroSection = () => {
  const navigate = useNavigate();

  const handleReserveClick = () => {
    navigate('/booking'); // <-- redirect path
  };

  return (
    <section className="hero">
      <article className="hero-text">
        <h1>Little Lemon</h1>
        <h3>Chicago</h3>
        <p>
          Family-owned Mediterranean restaurant serving traditional
          recipes with a modern twist.
        </p>
        <button className="btn-primary" onClick={handleReserveClick}>
          Reserve a Table
        </button>
      </article>
      <img
        className="hero-image"
        src={HeroImage}
        alt="Mediterranean food served at Little Lemon"
      />
    </section>
  );
};

export default HeroSection;
