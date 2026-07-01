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
        'The food tasted fresh, the service was warm, and the atmosphere felt relaxed without being too casual.',
    },
    {
      rating: 'Rating: ⭐️⭐️⭐️⭐️⭐️',
      photo: user2,
      name: 'Jane Smith',
      review:
        'The bruschetta and lemon dessert were excellent. Booking a table online was quick and simple.',
    },
    {
      rating: 'Rating: ⭐️⭐️⭐️⭐️⭐️',
      photo: user3,
      name: 'Aaron Durant',
      review:
        'A lovely neighborhood restaurant with generous portions and a menu that feels Mediterranean but modern.',
    },
    {
      rating: 'Rating: ⭐️⭐️⭐️⭐️⭐️',
      photo: user4,
      name: 'Rebecca Maya',
      review:
        'Great place for dinner with friends. The staff were helpful and the seasonal dishes were worth trying.',
    },
  ];
  return (
    <section className="testimonials">
      <h2>Testimonials</h2>
      <div className="testimonial-grid">
        {testimonials.map((testimonial, index) => (
          <article className="testimonial" key={index}>
            <p>{testimonial.rating}</p>
            <img src={testimonial.photo} alt={testimonial.name} />
            <h4>{testimonial.name}</h4>
            <p>{testimonial.review}</p>
          </article>
        ))}
      </div>
    </section>
  );
};

export default CustomerSay;
