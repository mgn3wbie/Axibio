import React, { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';

function DataViz() {
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
                    console.log("Unauthorized. You need to login or you don't have the rights to access this page...");
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
            <h2>Data Vizualisation of energy events</h2>
            
            {userData ? (
                <p id="homePageParagraph">
                    Hello {userData.username.substring(0, userData.username.indexOf('@'))}!
                </p>
            ) : (
                <p id="homePageParagraph">You are not logged in. Please log in to continue.</p>
            )}
            
        </div>
    );
}
export default DataViz;