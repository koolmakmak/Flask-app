import React, { useState, useEffect } from 'react';
import assets from '../assets/asset';
import './styles.css';
import {Link} from "react-router-dom";
import { Swiper, SwiperSlide } from 'swiper/react';
import { Navigation, Pagination, Scrollbar } from 'swiper/modules';
import { motion } from 'framer-motion'
import 'swiper/css';
import 'swiper/css/navigation';
import 'swiper/css/pagination';
import 'swiper/css/scrollbar';

const HomePage = () => {
  const [menuOpen, setMenuOpen] = useState(false);

  useEffect(() => {
    if (menuOpen) {
      document.body.classList.add("show-mobile-menu");
    } else {
      document.body.classList.remove("show-mobile-menu");
    }
  }, [menuOpen]);

  const openMenu = () => setMenuOpen(true);
  const closeMenu = () => setMenuOpen(false);

  return (
    <motion.div
      initial={{ opacity: 0, x: -50 }}
      animate={{ opacity: 1, x: 0 }}
      exit={{ opacity: 0, x: 50 }}
      transition={{ duration: 0.5 }}
    >
      <header>
        <nav className="navbar section-content">
          <a href="#" className="nav-logo">
            <h2 className="logo-text">🪴Plant</h2>
          </a>
          <ul className="nav-menu">
            <button id="menu-close-button" className="fas fa-times" onClick={closeMenu}></button>
            <li className="nav-item"><a href="#" className="nav-link">Home</a></li>
            <li className="nav-item"><a href="#about" className="nav-link">About</a></li>
            <li className="nav-item">
              <Link to="/check" className="nav-link">Check</Link>
            </li>
            <li className="nav-item"><a href="#organizer" className="nav-link">Organizer</a></li>
          </ul>
          <button id="menu-open-button" className="fas fa-bars" onClick={openMenu}></button>
        </nav>
      </header>

      <main>
        <section className="hero-section">
          <div className="section-content">
            <div className="hero-details">
              <h2 className="title">Let's garden</h2>
              <h3 className="subtitle">Before you grow, know your soil first!</h3>
              <p className="description">
                Discover the best plants for your garden with our AI-powered soil analysis tool.
                Get personalized recommendations and tips to help your garden thrive.
              </p>
              <div className="buttons">
                <Link to="/check" className="button get-started">Get Started</Link>
                <a href="#about" className="button learn-more">Learn More</a>
              </div>
            </div>
            <div className="hero-image-wrapper">
              <img src={assets.flower} alt="Hero" className="hero-image" />
            </div>
          </div>
        </section>

        <section className="about-section" id="about">
          <div className="section-content">
            <div className="about-image-wrapper">
              <img src={assets.about} alt="About" className="about-image" />
            </div>
            <div className="about-details">
              <h2 className="section-title">About Us</h2>
              <p className="text">
                We are a team of passionate gardeners and tech enthusiasts from KOSEN-KMITL dedicated
                to helping you grow the garden of your dreams. Our AI-powered soil analysis tool provides
                personalized recommendations based on your soil type by collecting data from sensors. Whether you're a beginner or an
                experienced gardener, we're here to support you every step of the way.
              </p>
              <div className="social-link-list">
                <a href="https://www.facebook.com/KOSENKMITL" className="social-link"><i className="fa-brands fa-facebook"></i></a>
                <a href="https://www.instagram.com/kosenkmitl_official/" className="social-link"><i className="fa-brands fa-instagram"></i></a>
              </div>
            </div>
          </div>
        </section>
        
        <section className="organizer-section" id="organizer">
          <h2 className="section-title">Organizer</h2>
          <div className="section-content">
            <div className="slider-container">
              <Swiper
                slidesPerView={2}
                direction="horizontal"
                loop={true}
                pagination={{ clickable: true }}
                navigation={true}
                modules={[Navigation, Pagination, Scrollbar]}
                className="organizer-list"
              >
                <SwiperSlide className="organizer">
                  <img src={assets.Warm} alt="User" className="user-image" />
                  <h3 className="name">Pannathorn Hanjirasawat</h3>
                </SwiperSlide>
                <SwiperSlide className="organizer">
                  <img src={assets.Minnie} alt="User" className="user-image" />
                  <h3 className="name">Thitima Chumsakol</h3>
                </SwiperSlide>
                <SwiperSlide className="organizer">
                  <img src={assets.Warm} alt="User" className="user-image" />
                  <h3 className="name">Pannathorn Hanjirasawat</h3>
                </SwiperSlide>
                <SwiperSlide className="organizer">
                  <img src={assets.Warm} alt="User" className="user-image" />
                  <h3 className="name">Pannathorn Hanjirasawat</h3>
                </SwiperSlide>
              </Swiper>
            </div>
          </div>
        </section>
      </main>
    </motion.div>
  );
};

export default HomePage;
