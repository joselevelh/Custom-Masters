import {BrowserRouter, Routes, Route} from 'react-router-dom';
import Navbar from "./Navigation/Navbar";
import Home from './pages/home';
import ManageFriends from "./pages/manage-friends";
import Login from "./pages/login";
import SignUp from "./pages/sign-up";
import MapView from "./pages/map-view";
import "bootstrap/dist/css/bootstrap.min.css";
import './App.css';
import {Provider} from 'react-redux';
import store from './store';

function App() {
    return (
        <Provider store={store}>
                <Navbar/>
                <BrowserRouter>
                    <Routes>
                        <Route path="/" element={<Home/>}/>
                        <Route exact path="/manage-friends" element={<ManageFriends/>}/>
                        <Route exact path="/login" element={<Login/>}/>
                        <Route exact path="/sign-up" element={<SignUp/>}/>
                        <Route exact path="/map-view" element={<MapView/>}/>
                    </Routes>
                </BrowserRouter>
        </Provider>
    );
}

export default App;
