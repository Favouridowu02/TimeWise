import { useAuth } from '../../contexts/AuthContext';
import { useState } from 'react';

const Login = () => {
  const { loginUser } = useAuth();
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      await loginUser({ email, password });
      // navigate to dashboard
    } catch (err) {
      console.error('Login failed');
    }
  };

  return (
    <>
    <h1>I am here</h1>
    <form onSubmit={handleSubmit}>
      <input value={email} onChange={(e) => setEmail(e.target.value)} placeholder="Email" />
      <input value={password} onChange={(e) => setPassword(e.target.value)} type="password" placeholder="Password" />
      <button type="submit">Login</button>
    </form>
    </>
  );
};

export default Login;
