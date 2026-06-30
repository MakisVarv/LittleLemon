import './App.css';
import HomePage from './components/HomePage';
import ReserveTable from './components/ReserveTable';
import { Route, Routes } from 'react-router-dom';
import Nav from './components/Nav';
import Footer from './components/Footer';
import ConfirmedBooking from './components/ConfirmedBooking';
import LoginPage from './pages/LoginPage';

function App() {
  return (
    <>
      <Nav />
      <Routes>
        <Route path="/" element={<HomePage />} />
        <Route path="/booking" element={<ReserveTable />} />
        <Route path="/confirmed" element={<ConfirmedBooking />} />
        <Route path="/login" element={<LoginPage />} />
      </Routes>
      <Footer />
    </>
  );
}

export default App;
