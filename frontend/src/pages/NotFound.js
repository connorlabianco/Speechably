import React from 'react';
import { Link } from 'react-router-dom';
import '../styles/pages/NotFound.css';

function NotFound() {
  return (
    <div className="not-found">
      <h1>404</h1>
      <h2>Page Not Found</h2>
      <p>The page you're looking for doesn't exist or has been moved.</p>
      <Link to="/" className="btn-primary">Go Home</Link>
    </div>
  );
}

export default NotFound;