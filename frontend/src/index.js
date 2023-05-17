import React from 'react';
import ReactDOM from 'react-dom/client';
import { BrowserRouter } from "react-router-dom";
import AppRoute from './config/app-route.jsx';

// bootstrap
import 'bootstrap';

// css
import '@react-pdf-viewer/core/lib/styles/index.css';
import '@fortawesome/fontawesome-free/css/all.css';
import './index.css';
import './scss/react.scss';

const root = ReactDOM.createRoot(document.getElementById('root'));
//function App() { return <AppRoute /> }

root.render(
  <React.StrictMode>
    <BrowserRouter>
      <AppRoute />
    </BrowserRouter>
  </React.StrictMode>
);