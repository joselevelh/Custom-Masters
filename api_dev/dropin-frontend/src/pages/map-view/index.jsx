import React, {useRef, useEffect, useState} from 'react';
import mapboxgl from '!mapbox-gl'; // eslint-disable-line import/no-webpack-loader-syntax
import useLocation from "../../custom-hooks/useLocation";
import SimpleMap from "../../components/Map/SimpleMap";
import PinInfoCard from "../../components/DropPinForm/DropPinForm";
import DropPinButton from "../../components/PinSessionButtons/StartPinSessionButton";
import EndPinSessionButton from "../../components/PinSessionButtons/EndPinSessionButton";


function MapView() {
    const userLocation = useLocation()
    const [showPinInfoCard, setShowPinInfoCard] = useState(false)
    const [activePinSession, setActivePinSession] = useState(false)
    const [pinInfo, setPinInfo] = useState("")

    // Event handler to toggle the visibility of the PinInfoCard
    function handleDropPin() {
        setShowPinInfoCard(!showPinInfoCard)
        setActivePinSession((!activePinSession))
    }

    function handlePinInfoChange(e){
        setPinInfo(e.target)
    }

    function handlePinInfoSubmit(e) {
        // TODO: Create pin object
        // TODO: Send pin object to map
        e.preventDefault()
        console.log("Submitting pin info: "+ pinInfo)

    }


    if (!activePinSession) {
        return (
            <div style={{display: 'flex', flexDirection: 'column', alignItems: 'center'}}>
                <div style={{position: 'relative'}}>
                    <SimpleMap userLocation={userLocation}/>
                    {showPinInfoCard && <PinInfoCard onChange={handlePinInfoChange} onSubmit = {handlePinInfoSubmit} />}
                </div>
                <DropPinButton onDropPin={handleDropPin}/>
            </div>
        );
    } else {
        return (
            <div style={{display: 'flex', flexDirection: 'column', alignItems: 'center'}}>
                <div style={{position: 'relative'}}>
                    <SimpleMap userLocation={userLocation}/>
                    {showPinInfoCard && <PinInfoCard/>}
                </div>
                <EndPinSessionButton onEndPinSession={handleDropPin}/>
            </div>
        );
    }
}

export default MapView
