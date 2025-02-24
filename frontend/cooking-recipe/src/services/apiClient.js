import axios from 'axios';


export const apiClient = axios.create({
  baseURL: 'https://172.31.178.54:8002', 
  headers: {
    'Content-Type': 'application/json',
    'Authorization': "Bearer " + localStorage.getItem('token')
  },
});

