import React, {useState, useEffect} from 'react';

const LocationComponent = () => {
    const [latitude, setLatitude] = useState(null);
    const [longitude, setLongitude] = useState(null);

    useEffect(() => {
        const retrieveLocation = () => {
            // Check if the browser supports geolocation
            if (navigator.geolocation) {
                navigator.geolocation.getCurrentPosition(
                    (position) => {
                        setLatitude(position.coords.latitude);
                        setLongitude(position.coords.longitude);
                    },
                    (error) => {
                        console.error(error);
                    }
                );
            } else {
                console.error('Geolocation is not supported by this browser.');
            }
        };
        retrieveLocation();
    }, []);

    return (
        <div>
            Latitude: {latitude}<br/>
            Longitude: {longitude}
        </div>
    );
};

export default LocationComponent;
