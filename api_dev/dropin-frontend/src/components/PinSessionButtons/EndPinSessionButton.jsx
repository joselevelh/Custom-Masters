import React from "react";

export default function EndPinSessionButton({onEndPinSession}) {
    return (<button type="button" className="btn btn-danger drop-button " onClick={onEndPinSession}>End Session</button>)
}