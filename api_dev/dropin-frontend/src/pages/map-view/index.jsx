import React from 'react';
import map_image from '../../map_image.png'
function MapView() {
    return(
        <>
            <p>Map View Page</p>
            <RenderMap/>
            <PinDropButton/>
        </>
        );
}

function RenderMap(){
    return (
        <>
            <img src={map_image} alt="still map of Washington DC"/>
        </>
    );
}

function PinDropButton(){
    function handleClick() {
    alert('You clicked me!');
    }
    return(
        <>
            <button type="button" className="btn btn-primary btn-lg btn-block" onClick={handleClick}>
                Drop pin at my location
            </button>
        </>
    );
}

export default MapView;