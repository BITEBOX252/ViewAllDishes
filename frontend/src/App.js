import { BrowserRouter, Route, Routes } from "react-router-dom";
import UserLogin from "./pages/auth/UserLogin";
import UserRegister from "./pages/auth/UserRegister";
import PrivateRoute from "./components/PrivateRoute";
import Dashboard from "./pages/Dashboard";
import Register from "./pages/Restaurant/Register";
import PrivateRoute from "./components/PrivateRoute";  // Import the PrivateRoute component
import RestaurantDashboard from "./pages/Restaurant/RestaurantDashboard";
import AddDish from "./pages/Restaurant/AddDish";
import Dish from "./pages/Restaurant/Dish";


function App() {
  
  
  return (
    <>
      <BrowserRouter>
        <Routes>
          <Route path="/login" element={<UserLogin />} />
          <Route path="/register" element={<UserRegister />} />
          <Route path="/restaurant-register" element={<Register />} />

          <Route path="/restaurant/dashboard" element={<PrivateRoute element={<RestaurantDashboard />} />} />
          <Route path="/restaurant/add-dish" element={<PrivateRoute element={<AddDish />} />} />
          <Route path="/restaurant/dishes" element={<PrivateRoute element={<Dish />} />} />


          <Route path="/dashboard" element={<PrivateRoute element={<Dashboard />} />} />

          <Route path="*" element={<h1>Error 404 Page not found !!</h1>} />
        </Routes>
      </BrowserRouter>
    </>
  );
}

export default App;
