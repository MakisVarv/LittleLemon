import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import {
  getBookingAvailability,
  createBooking,
} from '../services/bookings';

const ReserveTable = () => {
  const [formData, setFormData] = useState({
    firstName: '',
    lastName: '',
    date: '',
    time: '',
    diners: 1,
    occasion: '',
  });
  const navigate = useNavigate();
  const [errors, setErrors] = useState({});
  const [availableSlots, setAvailableSlots] = useState([]);
  const [availabilityError, setAvailabilityError] = useState('');
  const [isLoadingSlots, setIsLoadingSlots] = useState(false);
  const [submitError, setSubmitError] = useState('');
  const [isSubmitting, setIsSubmitting] = useState(false);

  // Validate inputs
  const validate = () => {
    const newErrors = {};
    if (
      !formData.firstName ||
      formData.firstName.length < 2 ||
      formData.firstName.length > 30
    ) {
      newErrors.firstName =
        'First name must be between 2 and 30 characters.';
    }
    if (
      !formData.lastName ||
      formData.lastName.length < 2 ||
      formData.lastName.length > 30
    ) {
      newErrors.lastName =
        'Last name must be between 2 and 30 characters.';
    }
    if (!formData.date) newErrors.date = 'Date is required.';
    if (!formData.time) newErrors.time = 'Time is required.';
    if (formData.diners < 1 || formData.diners > 8) {
      newErrors.diners = 'Number of diners must be between 1 and 8.';
    }
    if (!formData.occasion)
      newErrors.occasion = 'Occasion is required.';
    return newErrors;
  };

  const handleChange = (e) => {
    const { name, value } = e.target;

    setFormData((prev) => ({
      ...prev,
      [name]: value,
    }));

    if (name === 'date' && value) {
      setIsLoadingSlots(true);
      setAvailabilityError('');

      getBookingAvailability(value)
        .then((data) => {
          setAvailableSlots(data.available_slots);
        })
        .catch(() => {
          setAvailabilityError('Could not load available times.');
          setAvailableSlots([]);
        })
        .finally(() => {
          setIsLoadingSlots(false);
        });
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    const validationErrors = validate();
    setErrors(validationErrors);

    if (Object.keys(validationErrors).length > 0) {
      return;
    }

    const bookingData = {
      first_name: formData.firstName,
      reservation_date: formData.date,
      reservation_slot: Number(formData.time),
    };

    try {
      setIsSubmitting(true);
      setSubmitError('');

      await createBooking(bookingData);

      navigate('/confirmed');
    } catch (error) {
      const backendError =
        error.response?.data?.reservation_slot?.[0] ||
        error.response?.data?.first_name?.[0] ||
        error.response?.data?.reservation_date?.[0] ||
        'Could not create booking.';

      setSubmitError(backendError);
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <section className="reservation-container">
      <h1>Reserve a Table</h1>
      <form onSubmit={handleSubmit} className="reservation-form">
        <label>
          First Name
          <input
            type="text"
            name="firstName"
            value={formData.firstName}
            onChange={handleChange}
            required
          />
          {errors.firstName && (
            <p className="error">{errors.firstName}</p>
          )}
        </label>

        <label>Last Name</label>
        <input
          type="text"
          name="lastName"
          value={formData.lastName}
          onChange={handleChange}
          required
        />
        {errors.lastName && (
          <p className="error">{errors.lastName}</p>
        )}

        <label>
          Date of Reservation
          <input
            type="date"
            name="date"
            value={formData.date}
            onChange={handleChange}
            required
          />
          {errors.date && <p className="error">{errors.date}</p>}
        </label>

        <label>
          Time of Reservation
          <select
            name="time"
            value={formData.time}
            onChange={handleChange}
            required
          >
            <option value="">Select Time</option>
            {availableSlots.map((slot) => (
              <option key={slot} value={slot}>
                {slot}:00
              </option>
            ))}
          </select>
          {isLoadingSlots && <p>Loading available times...</p>}
          {availabilityError && (
            <p className="error">{availabilityError}</p>
          )}
          {errors.time && <p className="error">{errors.time}</p>}
        </label>

        <label>
          Number of Diners
          <input
            type="number"
            name="diners"
            min="1"
            max="8"
            value={formData.diners}
            onChange={handleChange}
            required
          />
          {errors.diners && <p className="error">{errors.diners}</p>}
        </label>

        <label>
          Occasion
          <select
            name="occasion"
            value={formData.occasion}
            onChange={handleChange}
            required
          >
            <option value="">Select Occasion</option>
            <option value="Birthday">Birthday</option>
            <option value="Anniversary">Anniversary</option>
          </select>
          {errors.occasion && (
            <p className="error">{errors.occasion}</p>
          )}
        </label>
        {submitError && <p className="error">{submitError}</p>}
        <button
          type="submit"
          className="submit-btn"
          disabled={isSubmitting}
        >
          {isSubmitting ? 'Reserving...' : 'Reserve'}
        </button>
      </form>
    </section>
  );
};

export default ReserveTable;
