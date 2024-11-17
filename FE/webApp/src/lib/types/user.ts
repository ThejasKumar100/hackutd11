import type { User } from '@auth0/auth0-spa-js';

export enum UserRole {
    ADMIN = 'admin',
    USER = 'user'
}

export interface ExtendedUser extends User {
    role?: UserRole;
}