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
            console.error(e);
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
                {requestUsers.map((user) => (
                    <li key={user.id}>{user.name}</li>
                ))}
            </ul>
        </div>
    );
}

