import React, {useEffect, useState} from 'react';
import GoogleMapReact from 'google-map-react';
import LocationComponent from "../../components/Location/Location";
import useLocation from "../../custom-hooks/useLocation";


function MapView() {
    const userLocation = useLocation()
    return (
        <>
            <p>Map View Page</p>
            <LocationComponent/>
            <SimpleMap location={userLocation}/>
        </>
    );
}

const AnyReactComponent = ({text}) => <div>{text}</div>;

function SimpleMap({location}) {
    let defaultProps;
    if (location) {
        console.log("Location passed into SimpleMap: "+ location)
        defaultProps = {
            center: {
                lat: location.latitude,
                lng: location.longitude,
            },
            zoom: 11,
        };
    } else {
        defaultProps = {
            center: {
                lat: 32.7157,
                lng: -117.1611,
            },
            zoom: 11,
        };
    }

    return (
        // Important! Always set the container height explicitly
        <div style={{margin: '0 auto', height: '80vh', width: '60%'}}>
            <GoogleMapReact
                bootstrapURLKeys={{key: "AIzaSyBIPjQHY2D5QEGVIqKz_KErsA8Sw-C95Gs"}}
                defaultCenter={defaultProps.center}
                defaultZoom={defaultProps.zoom}
            >
                <AnyReactComponent
                    lat={32.7157}
                    lng={-117.1611}
                    text="My Marker"
                />
            </GoogleMapReact>
        </div>
    );
}

export default MapView;