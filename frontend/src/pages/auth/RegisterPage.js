import { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { registerUser } from '../../services/auth';

const RegisterPage = () => {
  const navigate = useNavigate();
  const [formData, setFormData] = useState({
    username: '',
    email: '',
    password: '',
    re_password: '',
  });

  const [error, setError] = useState('');
  const [isSubmitting, setIsSubmitting] = useState(false);
  function handleChange(e) {
    const { name, value } = e.target;

    setFormData((prevData) => ({
      ...prevData,
      [name]: value,
    }));
  }
  async function handleSubmit(e) {
    e.preventDefault();
    setError('');
    if (formData.password !== formData.re_password) {
      setError('Passwords do not match');
      return;
    }
    setIsSubmitting(true);

    try {
      await registerUser(formData);
      navigate('/login');
    } catch (err) {
      setError('Registration failed. Please check your information.');
    } finally {
      setIsSubmitting(false);
    }
  }
  return (
    <main className="auth-page">
      <section className="auth-card">
        <h1>Create Account</h1>
        {error && <p className="form-error">{error}</p>}
        <form onSubmit={handleSubmit}>
          <input
            name="username"
            value={formData.username}
            onChange={handleChange}
            placeholder="Username"
            required
          />

          <input
            name="email"
            type="email"
            value={formData.email}
            onChange={handleChange}
            placeholder="Email"
            required
          />

          <input
            name="password"
            type="password"
            value={formData.password}
            onChange={handleChange}
            placeholder="Password"
            required
          />

          <input
            name="re_password"
            type="password"
            value={formData.re_password}
            onChange={handleChange}
            placeholder="Confirm password"
            required
          />

          <button type="submit" disabled={isSubmitting}>
            {isSubmitting ? 'Creating account...' : 'Register'}
          </button>
        </form>
        Already have an account? <Link to="/login">Log in</Link>
      </section>
    </main>
  );
};
export default RegisterPage;
