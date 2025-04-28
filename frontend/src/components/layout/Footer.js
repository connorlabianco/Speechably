import React from 'react';
import '../../styles/components/layout/Footer.css';

function Footer() {
  const currentYear = new Date().getFullYear();
  
  return (
    <footer className="footer">
      <div className="footer-container">
        <p>&copy; {currentYear} Speechably. All rights reserved.</p>
        <p>Created to help people improve their public speaking and communication skills.</p>
      </div>
    </footer>
  );
}

export default Footer;