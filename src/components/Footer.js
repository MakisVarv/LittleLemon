import React from "react";

const Footer = () => {
  return (
    <footer>
      <img src="#" alt="Logo" />

      <nav aria-label="Footer Navigation">
        <h4>Doormat Navigation</h4>
        <ul>
          <li><a href="#">Home</a></li>
          <li><a href="#">About</a></li>
          <li><a href="#">Menu</a></li>
          <li><a href="#">Reservations</a></li>
          <li><a href="#">Order Online</a></li>
          <li><a href="#">Login</a></li>
        </ul>
      </nav>

      <address>
        <h4>Contact</h4>
        <ul>
          <li>123 Main St, Chicago</li>
          <li>(312) 555-1234</li>
          <li>
            <a href="mailto:info@littlelemon.com">info@littlelemon.com</a>
          </li>
        </ul>
      </address>

      <section aria-label="Social Media Links">
        <h4>Social Media Links</h4>
        <ul>
          <li><a href="#">Facebook</a></li>
          <li><a href="#">Instagram</a></li>
          <li><a href="#">Twitter</a></li>
        </ul>
      </section>
    </footer>
  );
};

export default Footer;
