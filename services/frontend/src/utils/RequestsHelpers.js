export const getTokenOrRedirect = (navigate) => {
    const token = localStorage.getItem('token');
    if (!token) {
        navigate("/");
    }
    return token;
};

export const handleRequestFailure = (error, setErrorMessage, navigate) => {
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