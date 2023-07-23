import React, {useRef, useEffect, useState} from 'react';
import mapboxgl from '!mapbox-gl'; // eslint-disable-line import/no-webpack-loader-syntax
import useLocation from "../../custom-hooks/useLocation";
import SimpleMap from "../../components/Map/SimpleMap";

function MapView() {
    const userLocation = useLocation();
    return (
        <>
            <SimpleMap userLocation={userLocation}/>
        </>
    );
}

export default MapView;
