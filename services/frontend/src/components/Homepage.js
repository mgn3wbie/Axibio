import React, { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';

function LogButtons() {
    if (localStorage.getItem('token') !== null && localStorage.getItem('token') !== undefined) {
        return (
            <div className="logbuttons">
                <Link to="/data"><button className="padded-button">See the data</button></Link>
            </div>
        );
    }
    return (
        <div className="logbuttons">
            <Link to="/auth"><button className="padded-button">Log In or Sign Up</button></Link>
        </div>
    );
}

function Homepage() {
    const [userData, setUserData] = useState(null);
    useEffect(() => {
        const token = localStorage.getItem('token');
        // avoid the request if no token is set
        if (!token) {
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
                <p id="homePageParagraph">
                    You are not logged in. Please log in or sign up to continue.
                </p>
            )}
            
            <LogButtons />
        </div>
    );
}
export default Homepage;