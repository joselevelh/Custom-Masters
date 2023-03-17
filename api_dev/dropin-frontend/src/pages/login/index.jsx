import React, {useState} from 'react';
import LoginForm from "../../components/LoginForm/LoginForm";
import './index.css'
import apiClient from "../../client";

function Login() {
    const [loginForm, setLoginForm] = useState({email: '', password: ''});
    async function login(email, password) {
        try {
            const response = await apiClient.post('/login', loginForm);
            localStorage.setItem('accessToken', response.data.accessToken);
            return response.data;
        } catch (error) {
            throw error;
        }
    }
    function handleSubmit(e){
        e.preventDefault()
        console.log('Email:', loginForm.email)
        console.log('Password:', loginForm.password)

    }
    function handleChange(e){
        console.log("Test Change");
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