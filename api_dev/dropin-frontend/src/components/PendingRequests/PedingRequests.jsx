import React, {useEffect, useState} from "react";
import {apiClient} from "../../client";
import useAuthOrRedirect from "../../custom-hooks/useAuthOrRedirect";


export default function PendingRequests(){
    const [users, setUsers] = useState([])

    async function fetchFriendRequests() {
        try {
            const userList = await apiClient.get('/friends/requests?')
            setUsers(userList.data)
            console.log(users)
            return userList
        } catch (e) {
            console.error(e)
        }
    }
    useAuthOrRedirect("/login")
    useEffect(() =>{
        fetchFriendRequests()
    },[])
    return(
        <div className="friends-list">
            <h2>Pending Requests:</h2>
            <ul>
                {users.map(user => <li key={user.id}>{user.name}</li>)}
            </ul>
        </div>
    )
}