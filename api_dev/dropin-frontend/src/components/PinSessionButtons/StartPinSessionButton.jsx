import React from "react";

export default function DropPinButton({onDropPin}) {
    return (<button type="button" className="btn btn-primary drop-button " onClick={onDropPin}>Drop a pin to share your
        location!</button>)
}
