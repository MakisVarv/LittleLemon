import React from 'react';
import Logo from '../assets/Little-Lemon-Logo-circle-white.png';

const Footer = () => {
  return (
    <footer className="site-footer">
      <div className="footer-content">
        <div className="footer-brand">
          <img
            className="footer-logo"
            src={Logo}
            alt="Little Lemon logo"
          />
          <h3>Little Lemon</h3>
          <p>Family-owned Mediterranean restaurant in Chicago.</p>
          <p className="footer-copy">
            © 2026 Little Lemon. All rights reserved.
          </p>
        </div>

        <address className="footer-section footer-contact">
          <h4>Contact</h4>
          <ul>
            <li>123 Main St, Chicago</li>
            <li>(312) 555-1234</li>
            <li>
              <a href="mailto:info@littlelemon.com">
                info@littlelemon.com
              </a>
            </li>
          </ul>
        </address>

        <section
          className="footer-section"
          aria-label="Social Media Links"
        >
          <h4>Follow Us</h4>
          <ul>
            <li>
              <a href="#">Facebook</a>
            </li>
            <li>
              <a href="#">Instagram</a>
            </li>
            <li>
              <a href="#">Twitter</a>
            </li>
          </ul>
        </section>
      </div>
    </footer>
  );
};

export default Footer;
