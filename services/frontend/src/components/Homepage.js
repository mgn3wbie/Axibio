import React, { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';

function LogButtons() {
    if (localStorage.getItem('token') !== null) {
        return (
            <div className="logbuttons">
                {/* TODO : check how to logout user */}
                <Link to="/"><button className="padded-button">Log Me In</button></Link>
            </div>
        );
    }
    return (
        <div className="logbuttons">
            <Link to="/register"><button className="padded-button">Register Me</button></Link>
            <Link to="/login"><button className="padded-button">Log Me In</button></Link>
        </div>
    );
}
function Homepage() {
    const [userData, setUserData] = useState(null);
    useEffect(() => {
        // Fetch user data from the API endpoint
        fetch(`${process.env.REACT_APP_BACKEND_URL}/users/me`, {
            headers: {
                Authorization: `Bearer ${localStorage.getItem('token')}`,
            },
        })
        .then(response => response.json())
        .then(data => setUserData(data))
        .catch(error => console.error(error));
    }, []);
    const username = localStorage.getItem('username');
    return (
        <div>
        <h1 id="homePageTitle">Welcome to Axibio Technical Test</h1>
        
        <LogButtons />
         
        
        {userData && (
            <p>
            Welcome to the Homepage {username.substring(0, username.indexOf('@'))} - {process.env.REACT_APP_BACKEND_URL}!
            </p>
        )}
        </div>
    );
}
export default Homepage;