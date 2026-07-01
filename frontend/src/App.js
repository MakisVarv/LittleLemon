import './App.css';
import HomePage from './components/HomePage';
import ReserveTable from './components/ReserveTable';
import { Route, Routes, useNavigate } from 'react-router-dom';
import Nav from './components/Nav';
import Footer from './components/Footer';
import ConfirmedBooking from './components/ConfirmedBooking';
import LoginPage from './pages/LoginPage';
import { useState } from 'react';
import { getToken, removeToken } from './services/token';
import { logoutUser } from './services/auth';
import About from './pages/About';

function App() {
  const navigate = useNavigate();
  const [isAuthenticated, setIsAuthenticated] = useState(
    Boolean(getToken()),
  );
  const handleLoginSuccess = () => {
    setIsAuthenticated(true);
  };
  const handleLogout = async () => {
    try {
      await logoutUser();
    } finally {
      removeToken();
      setIsAuthenticated(false);
      navigate('/');
    }
  };
  return (
    <>
      <Nav
        isAuthenticated={isAuthenticated}
        onLogout={handleLogout}
      />
      <Routes>
        <Route path="/" element={<HomePage />} />
        <Route path="/about" element={<About />} />
        <Route path="/booking" element={<ReserveTable />} />
        <Route path="/confirmed" element={<ConfirmedBooking />} />
        <Route
          path="/login"
          element={<LoginPage onLoginSuccess={handleLoginSuccess} />}
        />
      </Routes>
      <Footer />
    </>
  );
}

export default App;
