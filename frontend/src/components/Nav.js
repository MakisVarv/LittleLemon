import React from 'react';
import { NavLink } from 'react-router-dom';
import Logo from '../assets/Logo.svg';

const Navbar = ({
  isAuthenticated,
  isManager,
  isDeliveryCrew,
  isCustomer,
  onLogout,
}) => {
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
          {isCustomer && (
            <li>
              <NavLink className="nav-link" to="/orders">
                My Orders
              </NavLink>
            </li>
          )}
          {isAuthenticated ? (
            <li>
              <button
                className="nav-link nav-button"
                type="button"
                onClick={onLogout}
              >
                Logout
              </button>
            </li>
          ) : (
            <li>
              <NavLink className="nav-link" to="/login">
                Login
              </NavLink>
            </li>
          )}
          <li>
            {isCustomer && (
              <NavLink className="nav-link" to="/cart">
                Cart
              </NavLink>
            )}
            {isManager && (
              <NavLink className="nav-link" to="/manager-dashboard">
                Dashboard
              </NavLink>
            )}
            {isDeliveryCrew && (
              <li>
                <NavLink className="nav-link" to="/delivery">
                  Deliveries
                </NavLink>
              </li>
            )}
          </li>
        </ul>
      </nav>
    </header>
  );
};

export default Navbar;
