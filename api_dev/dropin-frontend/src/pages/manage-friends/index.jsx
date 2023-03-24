import React from 'react';
import FriendsList from "../../components/FriendsList/FriendsList";
import AddFriend from "../../components/AddFriend/AddFriend";
import PendingRequests from "../../components/PendingRequests/PedingRequests";
function ManageFriends() {
    const TempEmail = "josefo1997@gmail.com"
    return(
        <>
            <h1>Manage Friends</h1>
            <p style={{color:"grey"}} >Psst...your email is: {TempEmail} </p>
            <AddFriend/>
            <PendingRequests/>
            <FriendsList/>
        </>
        );
}
export default ManageFriends;
