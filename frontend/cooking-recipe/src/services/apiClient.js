import axios from 'axios';


export const apiClient = axios.create({
  baseURL: import.meta.env.VITE_BACKEND_URL, 
  headers: {
    'Content-Type': 'application/json',
    'Authorization': `Bearer ${localStorage.getItem('accessToken')}`
  },
});

