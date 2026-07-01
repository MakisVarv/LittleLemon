import React from 'react';
import HeroSection from '../components/HeroSection';
import Specials from '../components/Specials';
import CustomerSay from '../components/CustomerSay';
import Chicago from '../components/Chicago';
import HomeHighlights from '../components/HomeHighlights';

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
