import { useEffect } from 'react';
import { useNavigate } from 'react-router-dom';

function Logout() {
    const navigate = useNavigate();

    useEffect(() => {
        // Clear localStorage and navigate to /
        localStorage.clear();
        navigate('/');
    }, [navigate]); // Run this effect once on component load

    return (
        <div>
            Logging out...
        </div>
    );
}
export default Logout;