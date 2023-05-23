import React from "react";

export default function AddFriend() {
    const TempEmail = "josefo1997@gmail.com"
    return (
        <>
            <p style={{color: "grey"}}>Psst...your email is: {TempEmail} </p>
            <h2>Add Friend:</h2>
            <AddFriendBox/>
        </>

    )
}
function AddFriendBox(){
    return (
        <div className="input-group mb-3 col-xs-2">
            <input type="text" className="form-control" placeholder="Add Friend by Email" aria-label="Recipient's username" aria-describedby="basic-addon2"/>
                <div className="input-group-append">
                    <button className="btn btn-outline-secondary" type="button">Send Request</button>
                </div>
        </div>
    )
}