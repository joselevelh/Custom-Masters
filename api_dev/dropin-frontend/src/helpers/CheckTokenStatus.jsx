import jwtDecode from "jwt-decode";

export default function checkTokenStatus() {
  try {
    const token = localStorage.getItem('accessToken');
    console.log('Has token:', token);
    const decoded = jwtDecode(token);

    if (decoded && decoded.exp && Date.now() < decoded.exp * 1000) {
      // Token is still valid
      console.log('User is logged in!');
      return true;
    } else {
      // Token has expired or is invalid
      console.log('User is not logged in!');
      return false;
    }
  } catch (e) {
    console.log(e);
  }
}