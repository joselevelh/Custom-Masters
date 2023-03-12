import React, {useEffect, useState} from 'react';
function ManageFriends() {
    return(
        <>
            <p>Manage Friends Page</p>
            <FriendsList/>
        </>
        );
}
function FriendsList() {
    const [users, setUsers] = useState([])
    const requestOptions = {
        method: "GET",
        // headers: { "Content-type": "application/json" },
        // body: JSON.stringify({ username, password })
    }
    async function fetchUserList() {
        try {
            const response = await fetch('http://127.0.0.1:8000/users/?skip=0&limit=100', requestOptions)
            const userList = await response.json()
            setUsers(userList)
            console.log(users)
            return userList
        } catch (e) {
            console.error(e)
        }
    }
    useEffect(() =>{
        fetchUserList()
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
export default ManageFriends;


