import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import SignInOrUp from './components/SignInOrUp';
import Homepage from './components/Homepage';
import Navbar from './components/Navbar';
import Logout from './components/Logout';
import DataViz from './components/DataViz';
import { AuthProvider } from './utils/AuthContext'
import './App.css'; // Import the styles.css file

// main application component and configuration of the routes using `react-router-dom`.
function App() {
  return (
    <Router>
    <AuthProvider>
    <Navbar />
      <div className="center-container">
      <Routes>
        <Route path="/" element={<Homepage />} />
        <Route path="/auth" element={<SignInOrUp />} />
        <Route path="/logout" element={<Logout />} />
        <Route path="/data" element={<DataViz />} />
      </Routes>
    </div>
    </AuthProvider>
    </Router>
  );
}
export default App;