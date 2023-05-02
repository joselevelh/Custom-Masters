import { configureStore } from '@reduxjs/toolkit';
import CheckTokenStatus from './helpers/CheckTokenStatus'

const initialState = {
  isAuthenticated: CheckTokenStatus()
};

function authReducer(state = initialState, action) {
  switch (action.type) {
    case 'LOGIN':
      console.log('Login dispatched to store')
      return {
        ...state,
        isAuthenticated: true,
      };
    case 'LOGOUT':
      console.log('Logout dispatched to store')
      return {
        ...state,
        isAuthenticated: false,
      };
    default:
      return state;
  }
}

const store = configureStore({
  reducer: {
    auth: authReducer
  }
});

export default store;
