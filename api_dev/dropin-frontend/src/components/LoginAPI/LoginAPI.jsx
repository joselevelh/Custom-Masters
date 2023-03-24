import {loginClient} from "../../client";
import React from "react";
export default async function login_api(email, password) {
        try {
            const usernameForm = {
                username: email,
                password: password,
            }
            const response = await loginClient.post('/token', usernameForm);
            console.log("Token Response:",response.data['access_token'])
            localStorage.setItem('accessToken', response.data['access_token']);
            return response.data;
        } catch (error) {
            throw error;
        }
    }