import './App.css';
import HomePage from './pages/HomePage';
import ReserveTable from './components/ReserveTable';
import { Route, Routes, useNavigate } from 'react-router-dom';
import Nav from './components/Nav';
import Footer from './components/Footer';
import ConfirmedBooking from './components/ConfirmedBooking';
import LoginPage from './pages/auth/LoginPage';
import { useEffect, useState } from 'react';
import { getCurrentUser, logoutUser } from './services/auth';
import { getToken, removeToken } from './services/token';
import About from './pages/About';
import RegisterPage from './pages/auth/RegisterPage';
import MenuPage from './pages/MenuPage';
import CartPage from './pages/CartPage';
import OrdersPage from './pages/OrdersPage';
import ManagerDashboardPage from './pages/ManagerDashboardPage';
import DeliveryDashboardPage from './pages/DeliveryDashboardPage';

function App() {
  const navigate = useNavigate();
  const [currentUser, setCurrentUser] = useState(null);
  const handleLoginSuccess = async () => {
    const user = await getCurrentUser();
    setCurrentUser(user);
  };
  const handleLogout = async () => {
    try {
      await logoutUser();
    } finally {
      removeToken();
      setCurrentUser(null);
      navigate('/');
    }
  };
  useEffect(() => {
    async function loadCurrentUser() {
      if (!getToken()) {
        return;
      }

      try {
        const user = await getCurrentUser();
        setCurrentUser(user);
      } catch {
        removeToken();
        setCurrentUser(null);
      }
    }

    loadCurrentUser();
  }, []);
  const isAuthenticated = Boolean(currentUser);
  const isManager = currentUser?.groups?.includes('Manager');
  const isDeliveryCrew =
    currentUser?.groups?.includes('Delivery crew');
  const isCustomer = isAuthenticated && !isManager && !isDeliveryCrew;
  return (
    <>
      <Nav
        isAuthenticated={isAuthenticated}
        isManager={isManager}
        isDeliveryCrew={isDeliveryCrew}
        isCustomer={isCustomer}
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
        <Route path="/register" element={<RegisterPage />} />
        <Route path="/menu" element={<MenuPage />} />
        <Route path="/cart" element={<CartPage />} />
        <Route path="/orders" element={<OrdersPage />} />
        <Route path="/delivery" element={<DeliveryDashboardPage />} />
        <Route
          path="/manager-dashboard"
          element={<ManagerDashboardPage />}
        />
      </Routes>
      <Footer />
    </>
  );
}

export default App;
