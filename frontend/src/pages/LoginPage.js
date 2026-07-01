import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { getCurrentUser, loginUser } from '../services/auth';
import { saveToken } from '../services/token';

const LoginPage = ({ onLoginSuccess }) => {
  const navigate = useNavigate();
  const [formData, setFormData] = useState({
    username: '',
    password: '',
  });

  const [error, setError] = useState('');
  const [isSubmitting, setIsSubmitting] = useState(false);
  const handleChange = (e) => {
    const { name, value } = e.target;

    setFormData((prev) => ({
      ...prev,
      [name]: value,
    }));
  };
  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      setIsSubmitting(true);
      setError('');
      const data = await loginUser(formData);
      saveToken(data.auth_token);
      onLoginSuccess();
      const user = await getCurrentUser();
      console.log('Logged in user:', user);
      navigate('/');
    } catch {
      setError('Invalid credentials');
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <section className="reservation-container">
      <h1>Login</h1>
      <form onSubmit={handleSubmit} className="reservation-form">
        <label>User Name</label>
        <input
          type="text"
          name="username"
          value={formData.username}
          onChange={handleChange}
          required
        />
        <label>Password</label>
        <input
          type="password"
          name="password"
          value={formData.password}
          onChange={handleChange}
          required
        />
        {error && <p className="error">{error}</p>}
        <button
          type="submit"
          className="submit-btn"
          disabled={isSubmitting}
        >
          {isSubmitting ? 'Logging in...' : 'Login'}
        </button>
      </form>
    </section>
  );
};
export default LoginPage;
