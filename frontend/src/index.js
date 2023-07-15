import React from 'react';
import ReactDOM from 'react-dom/client';
import AppRoute from './config/app-route.jsx';

// bootstrap
import 'bootstrap';

// css
import '@fortawesome/fontawesome-free/css/all.css';
import './assets/css/index.css';
import './scss/react.scss';

const root = ReactDOM.createRoot(document.getElementById('root'));

root.render(
  <React.StrictMode>
    <AppRoute />
  </React.StrictMode>
);