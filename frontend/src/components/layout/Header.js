// src/components/layout/Header.js
import React from 'react';
import { Link } from 'react-router-dom';
import '../../styles/components/layout/Header.css';

function Header() {
  return (
    <header className="header">
      <div className="header-container">
        <Link to="/" className="logo">
          <span className="logo-icon">🗣️</span>
          <span className="logo-text">Speechably</span>
        </Link>
        <nav className="main-nav">
          <ul>
            <li><Link to="/">Home</Link></li>
            <li><a href="https://github.com/your-username/speechably" target="_blank" rel="noopener noreferrer">GitHub</a></li>
          </ul>
        </nav>
      </div>
    </header>
  );
}

export default Header;