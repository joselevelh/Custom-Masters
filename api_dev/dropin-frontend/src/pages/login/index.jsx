import React, {useState} from 'react';
import LoginForm from "../../components/LoginForm/LoginForm";
import './index.css'

function Login() {
    const [loginForm, setLoginForm] = useState({email: '', password: ''});

    function onLogin(e){

    }
    return (
        <>
            <div className="row">
                <div className="col-md-1"></div>
                <div className="col-md-10">
                    <div className="form-container">
                        <LoginForm onSubmit = {(e)=> onLogin(e)}/>
                    </div>
                </div>
                <div className="col-md-1"></div>
            </div>
        </>
    );
}

export default Login;