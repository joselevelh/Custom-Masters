import React, {useEffect, useState} from "react";
import {apiClient} from "../../client";
import useAuthOrRedirect from "../../custom-hooks/useAuthOrRedirect";

export default function FriendsList() {
    const [users, setUsers] = useState([])

    async function fetchUserList() {
        try {
            const userList = await apiClient.get('users/?skip=0&limit=100')
            setUsers(userList.data)
            console.log(users)
            return userList
        } catch (e) {
            console.error(e)
        }
    }
    async function fetchFriendList() {
        try {
            const userList = await apiClient.get('users/?skip=0&limit=100')
            setUsers(userList.data)
            console.log(users)
            return userList
        } catch (e) {
            console.error(e)
        }
    }
    useAuthOrRedirect("/login")
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