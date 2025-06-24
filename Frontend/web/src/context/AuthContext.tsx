import React, {createContext, useState, useEffect, type ReactNode} from 'react';
import axios, { AxiosError } from axios;    

// Define types
interface User {
    id: string,
    email: string,
    username: string,
    password: string,
    language: string,
    profile_image: string,
    bio: string,
    email_verified: boolean,
    role: string,
}