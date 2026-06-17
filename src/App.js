import './App.css';
import HomePage from './components/HomePage';
import ReserveTable from './components/ReserveTable';
import { Route, Routes } from 'react-router-dom';
import Nav from './components/Nav';
import Footer from './components/Footer';
import { useReducer } from 'react';
import { fetchAPI, submitAPI } from './api';
import { useNavigate } from 'react-router-dom';
import ConfirmedBooking from './components/ConfirmedBooking';

// Initial available times
const initializeTimes = () => {
  const today = new Date();
  return fetchAPI(today);
  // return ["17:00", "18:00", "19:00", "20:00", "21:00", "22:00"];
};

// Reducer to update available times (later, add logic based on selected date)
const updateTimes = (state, action) => {
  switch (action.type) {
    case 'UPDATE_TIMES':
      // You could fetch API data here using action.date
      return fetchAPI(new Date(action.date));
    // return ["17:00", "18:00", "19:00", "20:00", "21:00", "22:00"];
    case 'BOOK_TIME':
      // remove chosen time from state
      return state.filter((time) => time !== action.time);
    default:
      return state;
  }
};

function App() {
  const [availableTimes, dispatch] = useReducer(
    updateTimes,
    [],
    initializeTimes,
  );

  const navigate = useNavigate();

  // submit function
  const submitForm = (formData) => {
    const success = submitAPI(formData);
    if (success) {
      navigate('/confirmed');
    }
  };

  return (
    <>
      <Nav />
      <Routes>
         <Route path="/" element={<HomePage />}></Route>
        <Route
          path="/booking"
          element={
            <ReserveTable
              submitForm={submitForm}
              availableTimes={availableTimes}
              dispatch={dispatch}
            />
          }
        ></Route>
        <Route path="/confirmed" element={<ConfirmedBooking />} />
      </Routes>
      <Footer />
    </>
  );
}

export default App;
