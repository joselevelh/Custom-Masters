import React from 'react';
import FriendsList from "../../components/FriendsList/FriendsList";
import AddFriend from "../../components/AddFriend/AddFriend";
import PendingRequests from "../../components/PendingRequests/PedingRequests";
import LoginForm from "../../components/LoginForm/LoginForm";

function ManageFriends() {
    return (
        <div className="row">
            <div className="col-md-2"></div>
            <div className="col-md-8">
                <h1>Manage Friends</h1>
                <AddFriend/>
                <PendingRequests/>
                <FriendsList/>
            </div>
            <div className="col-md-2"></div>
        </div>
    );
}

export default ManageFriends;
