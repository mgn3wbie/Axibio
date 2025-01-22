import React from 'react';
import { Link } from 'react-router-dom';
import { useAuth } from '../utils/AuthContext';

function Navbar() {
    const { isLoggedIn } = useAuth();
    return (
        <nav className="navbar">
        <ul>
        <li>
        <Link to="/">Home</Link>
        </li>
        {
            isLoggedIn && ( <li><Link to="/data">Data</Link></li> )
        }
        </ul>
            {
                isLoggedIn ? (
                <ul className="navRight">
                    <li><Link to="/logout">Logout</Link></li>
                </ul>
                ) : (
                <ul className="navRight">
                <li><Link to="/auth">Auth</Link></li>
                </ul>
            )}
        
        </nav>
    );
}
export default Navbar;