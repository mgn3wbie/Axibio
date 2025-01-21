import React from 'react';
import { Link } from 'react-router-dom';
function Navbar() {
    return (
        <nav className="navbar">
        <ul>
        <li>
        <Link to="/">Home</Link>
        </li>
        </ul>
        <ul className="navRight">
        <li>
        <Link to="/login">Login</Link>
        </li>
        <li>
        <Link to="/register">Register</Link>
        </li>
        </ul>
        </nav>
    );
}
export default Navbar;