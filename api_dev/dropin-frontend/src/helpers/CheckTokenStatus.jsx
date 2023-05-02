import jwtDecode from "jwt-decode";

export default function checkTokenStatus() {
  try {
    const token = localStorage.getItem('accessToken');
    console.log('Has token:', token);
    const decoded = jwtDecode(token);

    if (decoded && decoded.exp && Date.now() < decoded.exp * 1000) {
      // Token is still valid
      console.log('Token is valid!');
      return true;
    } else {
      // Token has expired or is invalid
      console.log('Token is invalid or does not exist!');
      return false;
    }
  } catch (e) {
    console.log(e);
    return false
  }
}