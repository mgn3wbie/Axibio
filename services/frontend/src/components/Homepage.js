import React, { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';

function LogButtons() {
    if (localStorage.getItem('token') !== null && localStorage.getItem('token') !== undefined) {
        return (
            <div className="logbuttons">
                {/* TODO : check how to logout user */}
                <Link to="/logout"><button className="padded-button">Log Me Out</button></Link>
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
        const token = localStorage.getItem('token');
        // avoid the request if no token is set
        if (!token) {
            console.log("No token found. User is not logged in.");
            return;
        }
        
        // Fetch user data from the API endpoint
        fetch(`${process.env.REACT_APP_BACKEND_URL}/users/me`, {
            headers: {
                Authorization: token,
            },
        })
        .then(response => {
            if (!response.ok) {
                if (response.status === 401) {
                    console.log("Unauthorized. You need to login...");
                    localStorage.clear();
                    setUserData(null);
                }
                throw new Error("Failed to fetch user data");
            }
            return response.json();
        })
        .then(data => setUserData(data))
        .catch(error => console.error(error));
    }, []);
    return (
        <div>
            <h1>Welcome to Axibio Technical Test</h1>
            
            {userData ? (
                <p id="homePageParagraph">
                    Hello {userData.username.substring(0, userData.username.indexOf('@'))}!
                </p>
            ) : (
                <p id="homePageParagraph">You are not logged in. Please log in to continue.</p>
            )}
            
            <LogButtons />
        </div>
    );
}
export default Homepage;