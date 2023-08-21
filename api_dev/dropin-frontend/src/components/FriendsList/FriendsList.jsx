import React, {useEffect, useState} from "react";
import {apiClient} from "../../client";
import useAuthOrRedirect from "../../custom-hooks/useAuthOrRedirect";

export default function FriendsList() {
    const [users, setUsers] = useState([])
    useAuthOrRedirect("/login")
     async function fetchFriendList() {
        try {
            const userList = await apiClient.get('/friends/accepted')
            setUsers(userList.data)
            console.log(users)
            return userList
        } catch (e) {
            console.error(e)
        }
    }
    useEffect(() =>{
        fetchFriendList()
    },[])
    return(
        <div className="friends-list">
            <h2>Friends:</h2>
            <ul>
                {users.map(user => <li key={user.id}>{user.name}</li>)}
            </ul>
        </div>
    )
}