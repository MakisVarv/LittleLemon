import React, { useState } from "react";

const ReserveTable = ({submitForm, availableTimes, dispatch }) => {
  const [formData, setFormData] = useState({
    firstName: "",
    lastName: "",
    date: "",
    time: "",
    diners: 1,
    occasion: "",
  });

  const [errors, setErrors] = useState({});

  // Validate inputs
  const validate = () => {
    const newErrors = {};
    if (!formData.firstName || formData.firstName.length < 2 || formData.firstName.length > 30) {
      newErrors.firstName = "First name must be between 2 and 30 characters.";
    }
    if (!formData.lastName || formData.lastName.length < 2 || formData.lastName.length > 30) {
      newErrors.lastName = "Last name must be between 2 and 30 characters.";
    }
    if (!formData.date) newErrors.date = "Date is required.";
    if (!formData.time) newErrors.time = "Time is required.";
    if (formData.diners < 1 || formData.diners > 8) {
      newErrors.diners = "Number of diners must be between 1 and 8.";
    }
    if (!formData.occasion) newErrors.occasion = "Occasion is required.";
    return newErrors;
  };

  // Handle input changes
  const handleChange = (e) => {
    const { name, value } = e.target;

    setFormData((prev) => ({
      ...prev,
      [name]: value,
    }));

    // If date changes → update available times
    if (name === "date") {
      dispatch({ type: "UPDATE_TIMES", date: value });
    }
  };

  // Handle form submission
  const handleSubmit = (e) => {
    e.preventDefault();
    const validationErrors = validate();
    setErrors(validationErrors);
    if (Object.keys(validationErrors).length === 0) {
      dispatch({ type: "BOOK_TIME", time: formData.time });
      submitForm(formData)
      // console.log("Form submitted:", formData);
      // alert("Booking confirmed!");
    }
  };

  return (
    <section className="reservation-container">
      <h1>Reserve a Table</h1>
      <form onSubmit={handleSubmit} className="reservation-form">
        {/* First name */}
        <label>
          First Name
          <input
            type="text"
            name="firstName"
            value={formData.firstName}
            onChange={handleChange}
            required
          />
          {errors.firstName && <p className="error">{errors.firstName}</p>}
        </label>

        {/* Last name */}
        <label>
          Last Name
          <input
            type="text"
            name="lastName"
            value={formData.lastName}
            onChange={handleChange}
            required
          />
          {errors.lastName && <p className="error">{errors.lastName}</p>}
        </label>

        {/* Date */}
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

        {/* Time */}
        <label>
          Time of Reservation
          <select
            name="time"
            value={formData.time}
            onChange={handleChange}
            required
          >
            <option value="">Select Time</option>
            {availableTimes.map((t) => (
              <option key={t} value={t}>
                {t}
              </option>
            ))}
          </select>
          {errors.time && <p className="error">{errors.time}</p>}
        </label>

        {/* Diners */}
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

        {/* Occasion */}
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
          {errors.occasion && <p className="error">{errors.occasion}</p>}
        </label>

        {/* Submit */}
        <button type="submit" className="submit-btn">
          Reserve
        </button>
      </form>
    </section>
  );
};

export default ReserveTable;
