import Mario_Adrian from '../assets/mario-and-adrian.jpg';

const About = () => {
  return (
    <section className="about-page">
      <article className="about-content">
        <h1>About Us</h1>

        <div className="about-layout">
          <div className="about-text">
            <p>
              Based in Chicago, Illinois, Little Lemon is a family
              owned Mediterranean restaurant, focused on traditional
              recipes served with a modern twist.
            </p>
            <p>
              The chefs draw inspiration from Italian, Greek, and
              Turkish culture and have a menu of 12-15 items that they
              rotate seasonally.
            </p>

            <p>
              The restaurant has a rustic and relaxed atmosphere with
              moderate prices, making it a popular place for a meal
              any time of the day.
            </p>

            <p>
              Little Lemon is owned by two Italian brothers, Mario and
              Adrian, who moved to the United States to pursue their
              shared dream of owning a restaurant.
            </p>

            <p>
              To craft the menu, Mario relies on family recipes and
              his experience as a chef in Italy.
            </p>

            <p>
              Adrian does all the marketing for the restaurant and led
              the effort to expand the menu beyond classic Italian to
              incorporate additional cuisines from the mediterranean
              region.
            </p>
          </div>

          <div className="about-image-column">
            <figure className="about-figure">
              <img src={Mario_Adrian} alt="Mario and Adrian" />
              <figcaption className="about-caption">
                Little Lemon owners Mario and Adrian.
              </figcaption>
            </figure>
          </div>
        </div>
      </article>
    </section>
  );
};
export default About;
