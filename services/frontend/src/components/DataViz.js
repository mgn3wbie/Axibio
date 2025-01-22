import React, { useEffect, useState } from 'react';
import axios from 'axios';
import JsonTable from './JsonTable';

function DataViz() {
    const [errorMessage, setErrorMessage] = useState('');
    const [eventData, setEventData] = useState(null); // Stockage des données

    // Fonction pour rafraîchir les données
    const handleRefresh = () => {
        const token = localStorage.getItem('token');
        if (!token) {
            console.log("No token found. User is not logged in.");
            return;
        }

        axios
            .post(`${process.env.REACT_APP_BACKEND_URL}/data/refresh`, null, {
                headers: {
                    Authorization: token,
                },
            })
            .then(response => {
                console.log("Data refreshed successfully");
                fetchData(); // Rafraîchir les données affichées après le succès
            })
            .catch(error => {
                if (error.response) {
                    setErrorMessage(error.response.data.detail || "Error while refreshing data.");
                } else if (error.request) {
                    setErrorMessage("No response from the server. Please try again.");
                } else {
                    setErrorMessage("Unexpected error occurred. Please try again.");
                }
            });
    };

    // Fonction pour récupérer les données utilisateur
    const fetchData = () => {
        const token = localStorage.getItem('token');
        if (!token) {
            console.log("No token found. User is not logged in.");
            return;
        }

        fetch(`${process.env.REACT_APP_BACKEND_URL}/data/events`, {
            headers: {
                Authorization: token,
            },
        })
        .then(response => {
            if (!response.ok) {
                if (response.status === 401) {
                    console.log("Unauthorized. You need to login or you don't have the rights to access this page...");
                }
                throw new Error("Failed to fetch data");
            }
            return response.json();
        })
        .then(data => {
            setEventData(data);
        })
        .catch(error => console.error(error));
    };

    // Fetch data when component is loaded
    useEffect(() => {
        fetchData();
    }, []);

    return (
        <div>
            <div>
                <h2>Data Visualization of Energy Events</h2>
                <button onClick={handleRefresh}>Refresh Data from Octave API</button>
            </div>
            {errorMessage && <p className="error">{errorMessage}</p>}

            <JsonTable data={eventData} />
        </div>
    );
}
export default DataViz;