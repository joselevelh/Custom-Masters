import React, {useEffect, useState} from "react";
import {apiClient} from "../../client";
import useAuthOrRedirect from "../../custom-hooks/useAuthOrRedirect";

export default function PendingRequests() {
    const [requests, setRequests] = useState([]);
    const [requestUsers, setRequestUsers] = useState([]);

    async function fetchFriendRequests() {
        try {
            const requestList = await apiClient.get('/friends/requests', { /* Add appropriate query parameters */});
            setRequests(requestList.data);
            console.log(requestList.data);
        } catch (e) {
            throw(e)
        }
    }

    async function convertRequestsToUsers() {
        try {
            const requestUserList = [];
            for (const request of requests) {
                try {
                    const user = await apiClient.get(`users/${request.sender}`);
                    requestUserList.push(user.data);
                } catch (error) {
                    console.error(`Error fetching user for request ID ${request.sender}:`, error);
                }
            }
            setRequestUsers(requestUserList);
            console.log(requestUserList);
        } catch (e) {
            console.error(e);
        }
    }

    const acceptRequest = async (requestId) => {
        // Handle accept logic here
        try {
            const response = await apiClient.patch(`friends/accept/${requestId}`);
        } catch (error) {
            console.log(`Error accepting request with id: ${requestId}`)
        }
        console.log(`Accepted friend request request ID: ${requestId}`);
        window.location.reload();
    };

    const declineRequest = async (requestId) => {
        // Handle decline logic here
        // Todo: Create api endpoint to delete friend Request (Decline) should be patch @ friends/accept/${userId}`
        console.log(`Declined friend request from request ID: ${requestId}`);
        window.location.reload();
    };

    useEffect(() => {
        fetchFriendRequests();
        // It's better to call convertRequestsToUsers() after the requests are fetched
    }, []);

    useEffect(() => {
        convertRequestsToUsers();
    }, [requests]); // Run the conversion when requests change

    useAuthOrRedirect("/login");

    return (
        <div className="friends-list">
            <h2>Pending Requests:</h2>
            <ul>
                {requestUsers.map((user, index) => (
                    <li key={user.id}>
                        {user.name}
                        <button className="btn btn-outline-primary btn-sm mx-1" onClick={() => acceptRequest(requests[index].id)}>Accept</button>
                        <button className="btn btn-outline-danger btn-sm"onClick={() => declineRequest(requests[index].id)}>Decline</button>
                    </li>
                ))}
            </ul>
        </div>
    );
}

