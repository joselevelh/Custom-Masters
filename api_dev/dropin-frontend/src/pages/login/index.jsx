import React, {useState} from 'react';
import { useNavigate } from 'react-router-dom';
import LoginForm from "../../components/LoginForm/LoginForm";
import './index.css'
import login_api from "../../components/LoginAPI/LoginAPI";
import {useDispatch} from "react-redux";


function Login() {
    const [loginForm, setLoginForm] = useState({email: '', password: ''});
    const navigate = useNavigate()
    const dispatch = useDispatch()
    async function handleSubmit(e){
        e.preventDefault()
        console.log('Email:', loginForm.email)
        console.log('Password:', loginForm.password)
        await login_api(loginForm.email, loginForm.password)
        const hasToken = localStorage.getItem('accessToken')
        console.log('Has token:', hasToken)
        if (hasToken){
            dispatch({ type: 'LOGIN' })
            navigate("/")
        }
        else{
            console.log('TODO: User facing error message')
        }
    }
    function handleChange(e){
        const { name, value } = e.target;
        setLoginForm({
            ...loginForm,
            [name]: value,
        })
    }
    return (
        <>
            <div className="row">
                <div className="col-md-1"></div>
                <div className="col-md-10">
                    <div className="form-container">
                        <LoginForm onChange={(e) => handleChange(e)} onSubmit = {(e) => handleSubmit(e)}  />
                    </div>
                </div>
                <div className="col-md-1"></div>
            </div>
        </>
    );
}

export default Login;