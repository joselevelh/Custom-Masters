import React, {useEffect, useRef, useState} from "react";
import mapboxgl from "mapbox-gl";


mapboxgl.accessToken = 'pk.eyJ1Ijoiam9zZWZvMTk5NyIsImEiOiJjbGp5emxjYncwMWxhM2dvNDdmaWp5dWFkIn0.NlylS3S5YnEYHQ6JyAR-HA';

function addPinsToMap(pins, mapObject){
    for (const pin in pins){
                const marker = new mapboxgl.Marker({
                color: "#e1c4ff"
            })
                .setLngLat([pins[pin][0],pins[pin][1]])
                .setPopup(new mapboxgl.Popup().setHTML("<h1>"+pins[pin][2]+"</h1>"))
                .addTo(mapObject.current);
            }
}

export default function SimpleMap({userLocation, activePins}) {
    const mapContainer = useRef(null);
    const map = useRef(null);
    const [lng, setLng] = useState(null); // Initialize with null
    const [lat, setLat] = useState(null); // Initialize with null
    const [zoom, setZoom] = useState(11.8);
    const dummyPins = {"Jake":[-117.15, 32.7,"Jake's Pin"], "Alexa":[-117.1771, 32.6928,"Alexa's Pin"] }

    useEffect(() => {
        if (!userLocation.latitude || !userLocation.longitude) return; // Wait for userLocation to be available

        if (!map.current) {
            map.current = new mapboxgl.Map({
                container: mapContainer.current,
                style: 'mapbox://styles/mapbox/streets-v12',
                center: [userLocation.longitude, userLocation.latitude], // Use user's location here
                zoom: zoom
            });
            addPinsToMap(dummyPins,map)
            map.current.on('move', () => {
                setLng(map.current.getCenter().lng.toFixed(4));
                setLat(map.current.getCenter().lat.toFixed(4));
                setZoom(map.current.getZoom().toFixed(2));
            });
        }
    }, [userLocation.latitude, userLocation.longitude, zoom]);


    return (
        <div align="center">
            <div className="sidebar">
                {userLocation.latitude && userLocation.longitude ? (
                    <>Longitude: {lng} | Latitude: {lat} | Zoom: {zoom}</>
                ) : (
                    <>Waiting for user location...</>
                )}
            </div>
            <div ref={mapContainer} className="map-container"/>
        </div>
    );
}