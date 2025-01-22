import React from 'react';
import { Link } from 'react-router-dom';
function Navbar() {
    return (
        <nav className="navbar">
        <ul>
        <li>
        <Link to="/">Home</Link>
        </li>
        {
            localStorage.getItem('token') !== null && localStorage.getItem('token') !== undefined
            &&
            <li>
                <Link to="/data">Data</Link>
            </li>
        }
        </ul>
            {
                localStorage.getItem('token') !== null && localStorage.getItem('token') !== undefined ?
                <ul className="navRight">
                    <li><Link to="/logout">Logout</Link></li>
                </ul>
                :
                <ul className="navRight">
                <li><Link to="/auth">Auth</Link></li>
                </ul>
            }
        
        </nav>
    );
}
export default Navbar;