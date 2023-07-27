import React, {useRef, useEffect, useState} from 'react';
import mapboxgl from '!mapbox-gl'; // eslint-disable-line import/no-webpack-loader-syntax
import useLocation from "../../custom-hooks/useLocation";
import SimpleMap from "../../components/Map/SimpleMap";

function PinInfoCard() {
    return (
        <div className="pinInfo card" style={{width: "18rem"}}>
            <div className="card-body">
                <h5 className="Pin Title">Jose's Pin</h5>
                <div className="form-group">
                    <label htmlFor="exampleFormControlTextarea1">Describe what your up to!</label>
                    <textarea className="form-control" id="exampleFormControlTextarea1" rows="3"></textarea>
                </div>
            </div>
        </div>
    )
}

function DropPinButton({onDropPin}) {
    return (<button type="button" className="btn btn-primary " onClick={onDropPin}>Drop a pin to share your
        location!</button>)
}

function MapView() {
    const userLocation = useLocation()
    const [showPinInfoCard, setShowPinInfoCard] = useState(false);

    // Event handler to toggle the visibility of the PinInfoCard
    const handleDropPin = () => {
        setShowPinInfoCard(!showPinInfoCard);
    };

    return (
        <div style={{display: 'flex', flexDirection: 'column', alignItems: 'center'}}>
            <div style={{position: 'relative'}}>
                <SimpleMap userLocation={userLocation}/>
                {showPinInfoCard && <PinInfoCard/>}
            </div>
            <DropPinButton onDropPin={handleDropPin}/>
        </div>
    );
}

export default MapView;
