import axios from './api';

export const login = async (credentials: { email: string; password: string }) => {
    try {
        const response = await axios.post('/auth/login', credentials, {
            headers: {
                'Content-Type': 'application/json',
            },
            withCredentials: true, // Include cookies in the request
        });
        return response.data;
    } catch (error) {
        if (axios.isAxiosError(error)) {
            throw new Error(error.response?.data?.message || 'Login failed');
        } else {
            throw new Error('An unexpected error occurred during login');
        }
    }
};

export const logout = async () => {
    
