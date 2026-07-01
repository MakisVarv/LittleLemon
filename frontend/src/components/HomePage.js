import React from 'react';
import HeroSection from './HeroSection';
import Specials from './Specials';
import CustomerSay from './CustomerSay';
import Chicago from './Chicago';
import HomeHighlights from './HomeHighlights';

const HomePage = () => {
  return (
    <main>
      <HeroSection />
      <HomeHighlights />
      <Specials />
      <CustomerSay />
      <Chicago />
    </main>
  );
};

export default HomePage;
