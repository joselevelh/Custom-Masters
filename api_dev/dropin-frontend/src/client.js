import axios from 'axios';
import CheckTokenStatus from '../src/helpers/CheckTokenStatus'
export const apiClient = axios.create({
  baseURL: 'http://127.0.0.1:8000',
  headers: {
    'Content-Type': 'application/json'
  }
});

// Add Authorization header with bearer token
if (CheckTokenStatus()) {
  const token = localStorage.getItem('accessToken');
  apiClient.defaults.headers.common['Authorization'] = `Bearer ${token}`;
}

export const loginClient = axios.create({
  baseURL: 'http://127.0.0.1:8000',
  headers: {
    'Content-Type': 'application/x-www-form-urlencoded'
  }
});

