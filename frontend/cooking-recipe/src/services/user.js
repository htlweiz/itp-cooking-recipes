
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
  