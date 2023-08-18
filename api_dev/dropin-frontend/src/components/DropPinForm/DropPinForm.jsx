import React from "react";

export default function PinInfoCard({onChange, onSubmit}) {
    return (
        <div className="pin-info-card" style={{width: "18rem"}}>
            <div className="card-body">
                <h5 className="Pin Title">Jose's Pin</h5>
                <form className="form-group" onChange={onChange} onSubmit={onSubmit}>
                    <label htmlFor="exampleFormControlTextarea1">Describe what your up to!</label>
                    <textarea className="form-control" id="exampleFormControlTextarea1" rows="3"></textarea>
                    <button type="submit" className="btn btn-primary">Start Session</button>
                </form>
            </div>
        </div>
    )
}