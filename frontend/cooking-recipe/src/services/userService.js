
export function isAuthenticated() {
  return !!localStorage.getItem('token');
}

export function login(token, email) {
  localStorage.setItem('token', token);
  localStorage.setItem('email', email);
}

export function logout() {
  localStorage.removeItem('token');
  localStorage.removeItem('email');
}

import { apiClient } from './apiClient';

export default {
getUsers() {
  return apiClient.get('/users/');
},
getUser(id) {
  return apiClient.get(`/users/${id}`);
},
createUser(user) {
  return apiClient.post('/users/', user);
},
updateUser(id, user) {
  return apiClient.put(`/users/${id}`, user);
},
deleteUser(id) {
  return apiClient.delete(`/users/${id}`);
},
readUserinfo() {
  return apiClient.get('/users/me');
},
login(email, password) {
  localStorage.setItem('email', email);
  localStorage.setItem('token', 'mock');
  return apiClient.post('/login', { email: email, password: password });
},
logout() {
  localStorage.removeItem('token');
  localStorage.removeItem('email');
  return apiClient.post('/logout');
},
getToken () {
  return localStorage.getItem('token');
}
};
  
