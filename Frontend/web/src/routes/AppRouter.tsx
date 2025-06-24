import { Route, Routes } from 'react-router-dom';

import { Login } from '../pages/Auth/Login';
import { Signup } from '../pages/Auth/Signup';
import { ResetPassword } from '../pages/Auth/ResetPassword'; // Uncomment if this file exists and has a named export
import { VerifyEmail } from '../pages/Auth/VerifyEmail'; // Uncomment if needed

const AppRouter = () => (
  <Routes>
	<Route path="/login" element={<Login />} />
	<Route path="/signup" element={<Signup />} />
	<Route path="/reset-password" element={<ResetPassword />} />
    <Route path="/verify-email" element={<VerifyEmail />} />
    
  </Routes>
);

export default AppRouter;
