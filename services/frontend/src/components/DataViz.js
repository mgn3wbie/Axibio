import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';
import JsonTable from './JsonTable';

function DataViz() {
    const [errorMessage, setErrorMessage] = useState('');
    const [eventData, setEventData] = useState(null);
    const navigate = useNavigate();

    const getTokenOrRedirect = () => {
        const token = localStorage.getItem('token');
        if (!token) {
            navigate("/");
        }
        return token;
    };

    const handleRequestFailure = (error, setErrorMessage) => {
        if (error.response) {
            setErrorMessage(error.response.data.detail || "Error while refreshing data.");
        } else if (error.request) {
            setErrorMessage("No response from the server. Please try again.");
        } else {
            setErrorMessage("Unexpected error occurred. Please try again.");
        }
        if (error.response.status === 401) {
            localStorage.clear();
            setTimeout(() => {
                navigate("/");
            }, 3000);
        }
    };

    const handleRefresh = () => {
        const token = getTokenOrRedirect();

        axios.post(`${process.env.REACT_APP_BACKEND_URL}/data/refresh`, null, {
            headers: {
                Authorization: token,
            },
        })
        .then(response => {
            // Refresh data on the front once the server is done
            // Any error is caught in the block below
            fetchData(); 
        })
        .catch(error => handleRequestFailure(error, setErrorMessage));
    };

    const fetchData = () => {
        const token = getTokenOrRedirect();

        axios.get(`${process.env.REACT_APP_BACKEND_URL}/data/events`, {
            headers: {
                Authorization: token,
            },
        })
        .then(response => {
            setEventData(response.data);
        })
        .catch(error => handleRequestFailure(error, setErrorMessage));
    };

    // Fetch data when component is loaded
    useEffect(() => {
        fetchData();
    }, []);

    return (
        <div>
            <div id="dataviz-title">
                <h2>Data Visualization of Energy Events</h2>
                <button onClick={handleRefresh} className="padded-button">Refresh Data from Octave API</button>
            </div>
            {errorMessage && <p className="error">{errorMessage}</p>}

            <JsonTable data={eventData} />
        </div>
    );
}
export default DataViz;