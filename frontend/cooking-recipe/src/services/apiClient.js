import axios from 'axios';


export const apiClient = axios.create({
  baseURL: 'https://localhost:8002', 
  headers: {
    'Content-Type': 'application/json',
    'Authorization': `Bearer ${localStorage.getItem('accessToken')}`
  },
});

