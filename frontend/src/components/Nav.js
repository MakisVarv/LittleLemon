import React from 'react';
import { NavLink } from 'react-router-dom';
import Logo from '../assets/Logo.svg';

const Navbar = ({ isAuthenticated, onLogout }) => {
  const navLinkClass = ({ isActive }) =>
    isActive ? 'nav-link active' : 'nav-link';
  return (
    <header className="site-header">
      <img className="site-logo" src={Logo} alt="Little Lemon logo" />
      <nav className="main-nav">
        <ul className="main-nav-list">
          <li>
            <NavLink className="nav-link" to="/">
              Home
            </NavLink>
          </li>
          <li>
            <NavLink className="nav-link" to="/about">
              About
            </NavLink>
          </li>
          <li>
            <NavLink className="nav-link" to="/menu">
              Menu
            </NavLink>
          </li>
          <li>
            <NavLink className="nav-link" to="/booking">
              Reservations
            </NavLink>
          </li>
          <li>
            <a href="#">Order Online</a>
          </li>
          <li>
            {isAuthenticated ? (
              <button
                className="nav-link nav-button"
                type="button"
                onClick={onLogout}
              >
                Logout
              </button>
            ) : (
              <NavLink className="nav-link" to="/login">
                Login
              </NavLink>
            )}
          </li>
        </ul>
      </nav>
    </header>
  );
};

export default Navbar;
