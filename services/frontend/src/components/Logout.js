import { useEffect } from 'react';
import { useNavigate } from 'react-router-dom';

function Logout() {
    const navigate = useNavigate();

    useEffect(() => {
        // Clear localStorage and navigate to the root
        localStorage.clear();
        navigate('/');
    }, [navigate]); // Run this effect once on component mount

    return (
        <div>
            Logging out...
        </div>
    );
}
export default Logout;