import React from 'react';
import user1 from '../assets/user1.jpg';
import user2 from '../assets/user2.jpg';
import user3 from '../assets/user3.jpg';
import user4 from '../assets/user4.jpg';

const CustomerSay = () => {
  const testimonials = [
    {
      rating: 'Rating: ⭐️⭐️⭐️⭐️⭐️',
      photo: user1,
      name: 'John Doe',
      review:
        'Sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.',
    },
    {
      rating: 'Rating: ⭐️⭐️⭐️⭐️⭐️',
      photo: user2,
      name: 'Jane Smith',
      review:
        'Sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.',
    },
    {
      rating: 'Rating: ⭐️⭐️⭐️⭐️⭐️',
      photo: user3,
      name: 'Aaron Durant',
      review:
        'Sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.',
    },
    {
      rating: 'Rating: ⭐️⭐️⭐️⭐️⭐️',
      photo: user4,
      name: 'Rebecca Maya',
      review:
        'Sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.',
    },
  ];
  return (
    <section className="testimonials">
      <h2>Testimonials</h2>
      <section className="testimonial-grid">
        {testimonials.map((testimonial, index) => (
          <article className="testimonial" key={index}>
            <p>{testimonial.rating}</p>
            <img src={testimonial.photo} alt={testimonial.name} />
            <h4>{testimonial.name}</h4>
            <p>{testimonial.review}</p>
          </article>
        ))}
      </section>
    </section>
  );
};

export default CustomerSay;
