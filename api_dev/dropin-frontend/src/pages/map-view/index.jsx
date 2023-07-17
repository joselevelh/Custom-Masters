import React from 'react';
import LocationComponent from "../../components/Location/Location";
import useLocation from "../../custom-hooks/useLocation";
import Map, {GeolocateControl} from "react-map-gl";
import "mapbox-gl/dist/mapbox-gl.css";


function MapView() {
    const userLocation = useLocation()
    return (
        <>
            <p>Map View Page</p>
            <LocationComponent/>
            <SimpleMap/>
        </>
    );
}

function SimpleMap() {
    return (
        <div>
            <Map
                mapboxAccessToken="pk.eyJ1Ijoiam9zZWZvMTk5NyIsImEiOiJjbGp5emxjYncwMWxhM2dvNDdmaWp5dWFkIn0.NlylS3S5YnEYHQ6JyAR-HA"
                initialViewState={{
                    longitude: -100,
                    latitude: 40,
                    zoom: 3.5,
                }}
                mapStyle="mapbox://styles/mapbox/streets-v11"
            >
                <GeolocateControl
                    positionOptions={{enableHighAccuracy: true}}
                    trackUserLocation={true}
                />
            </Map>
        </div>
    );
}


export default MapView;