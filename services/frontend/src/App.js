import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Login from './components/Login';
import Register from './components/Register';
import Homepage from './components/Homepage';
import Navbar from './components/Navbar';
import Logout from './components/Logout';
import './App.css'; // Import the styles.css file

// main application component and configuration of the routes using `react-router-dom`.
function App() {
  return (
    <Router>
    <Navbar />
    <div className="center-container">
    <Routes>
    <Route path="/" element={<Homepage />} />
    <Route path="/login" element={<Login />} />
    <Route path="/register" element={<Register />} />
    <Route path="/logout" element={<Logout />} />
    </Routes>
    </div>
    </Router>
  );
}
export default App;