import api from './api';
import axios from 'axios';


export const login = async (credentials: { email: string; password: string }) => {
    try {
        const response = await api.post('/auth/login', credentials, {
            headers: {
                'Content-Type': 'application/json',
            },
            withCredentials: true, // Include cookies in the request
        });
        return response.data;
    } catch (error: unknown) {
        if (axios.isAxiosError(error)) {
            throw new Error(error.response?.data?.message || 'Login failed');
        } else {
            throw new Error('An unexpected error occurred during login');
        }
    }
};


export const logout = async () => {
    try {
        const response = await api.post('/auth/logout', {}, {
            headers: {
                'Content-Type': 'application/json',
            },
            withCredentials: true, // Include cookies in the request
        });
        return response.data;
    } catch (error: unknown) {
        if (axios.isAxiosError(error)) {
            throw new Error(error.response?.data?.message || 'Logout failed');
        } else {
            throw new Error('An unexpected error occurred during logout');
        }
    }
}


export const getCurrentUser = async () => {
    const response = await api.get('/auth/me', {withCredentials: true});
    return response.data;
};