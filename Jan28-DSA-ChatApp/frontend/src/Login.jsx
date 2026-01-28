import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';
import WoodyKey from './components/WoodyKey';

const Login = () => {
  const [isRegister, setIsRegister] = useState(false);
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const navigate = useNavigate();

  const handleAuth = async (e) => {
    e.preventDefault();
    setError('');
    try {
      const endpoint = isRegister ? 'register' : 'login';
      const res = await axios.post(`${import.meta.env.VITE_API_URL}/auth/${endpoint}`, {
        username,
        password
      });

      if (!isRegister) {
        localStorage.setItem('token', res.data.access_token);
        localStorage.setItem('user_id', res.data.user_id);
        localStorage.setItem('username', res.data.username);
        navigate('/chat');
      } else {
        setIsRegister(false);
        setError("Account created! Please log in.");
      }
    } catch (err) {
      console.error(err);
      if (err.response?.data?.detail) {
          const detail = err.response.data.detail;
          if (Array.isArray(detail)) {
              setError(detail.map(e => e.msg).join(', '));
          } else {
              setError(String(detail));
          }
      } else {
          setError("Authentication failed");
      }
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-[#F4F1EA] pattern-paper">
      <div className="bg-white p-10 rounded-2xl shadow-xl w-96 border border-[#E0Dcd0]">
        <div className="w-16 h-16 bg-[#8FB359] rounded-2xl mx-auto mb-6 flex items-center justify-center shadow-lg">
            <span className="text-white text-2xl font-bold">CC</span>
        </div>
        
        <h2 className="text-2xl font-bold mb-8 text-center text-[#2B2B2B]">
            {isRegister ? 'Create Account' : 'Welcome Back'}
        </h2>

        {error && (
          <div className="bg-red-50 border border-red-200 text-red-600 px-4 py-3 rounded-lg mb-6 text-sm">
            {error}
          </div>
        )}

        <form onSubmit={(e) => e.preventDefault()}>
          <div className="mb-4">
            <label className="block text-xs font-bold text-[#9CA3AF] uppercase mb-1">Username</label>
            <input 
              className="zen-input h-12"
              value={username}
              onChange={e => setUsername(e.target.value)}
              placeholder="Enter your username"
            />
          </div>

          <div className="mb-6">
            <label className="block text-xs font-bold text-[#9CA3AF] uppercase mb-1">Password</label>
            <input 
              type="password"
              className="zen-input h-12"
              value={password}
              onChange={e => setPassword(e.target.value)}
              placeholder="••••••••"
            />
          </div>

          <button 
            onClick={handleAuth} 
            className="zen-button w-full h-12 text-lg"
          >
            {isRegister ? 'Sign Up' : 'Log In'}
          </button>
        </form>
        
        <p className="mt-6 text-center text-[#9CA3AF] text-sm">
            {isRegister ? "Already have an account? " : "New to ChitChat? "}
            <button 
                className="text-[#8FB359] font-bold hover:underline"
                onClick={() => setIsRegister(!isRegister)}
            >
                {isRegister ? 'Log In' : 'Sign Up'}
            </button>
        </p>
      </div>
    </div>
  );
};

export default Login;
