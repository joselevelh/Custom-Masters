import React from "react";
import {apiClient} from "../../client";
import { useState } from 'react'; // Import the useState hook

export default function AddFriend() {
    const TempEmail = "josefo1997@gmail.com";
    const [message, setMessage] = useState(null); // State for success/failure message

    async function handleAddFriendSubmit(e) {
        e.preventDefault();
        const recipientEmail = e.target[0].value;

        try {
            const response = await apiClient.post(`friends/add/${recipientEmail}`);
            console.log(response);
            setMessage("Friend added successfully!"); // Set success message
            e.target.reset(); // Reset the form
        } catch (error) {
            console.log(error);
            setMessage("Failed to add friend."); // Set failure message
        }
    }

    return (
        <>
            <p style={{ color: "grey" }}>Psst...your email is: {TempEmail} </p>
            <h2>Add Friend:</h2>
            {message && <div className={`alert ${message.startsWith("Failed") ? "alert-danger" : "alert-success"}`} role="alert">
                {message}
            </div>}
            <AddFriendBox onSubmit={handleAddFriendSubmit} />
        </>
    )
}

function AddFriendBox({ onSubmit }) {
    return (
        <form onSubmit={onSubmit}>
            <div className="input-group mb-3 col-xs-2">
                <input type="text" className="form-control" placeholder="Add Friend by Email"
                       aria-label="Recipient's username" aria-describedby="basic-addon2" />
                <div className="input-group-append">
                    <button className="btn btn-outline-secondary" type="submit">Send Request</button>
                </div>
            </div>
        </form>
    )
}
