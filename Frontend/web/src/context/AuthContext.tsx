import React, {createContext, useState, useEffect, type ReactNode} from 'react';
import axios, { AxiosError } from axios;

// Define types
interface User {
    id: string,
    email: string,
    username: string,
    password: ,
    language: ,
    profile_image: ,
    bio: ,
    email_verified: ,
    role: ,
}