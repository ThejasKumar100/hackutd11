import { writable, get, type Writable } from 'svelte/store';
import { Auth0Client, type User, type LogoutOptions } from '@auth0/auth0-spa-js';
import { browser } from '$app/environment';
import { authConfig } from './auth-config';

// Define types
type AuthStore = Writable<Auth0Client | null>;
type UserStore = Writable<(User & { role?: UserRole }) | null>;
type ErrorStore = Writable<Error | null>;
type UserRole = 'admin' | 'user';   // admin & user type;


// Initialize stores with proper types
const createAuthStore = (): AuthStore => {
    const { subscribe, set, update } = writable<Auth0Client | null>(null);
    return {
        subscribe,
        set,
        update
    };
};

const createUserStore = (): UserStore => {
    const { subscribe, set, update } = writable<User | null>(null);
    return {
        subscribe,
        set,
        update
    };
};

const createErrorStore = (): ErrorStore => {
    const { subscribe, set, update } = writable<Error | null>(null);
    return {
        subscribe,
        set,
        update
    };
};

export const auth0Client = createAuthStore();
export const isAuthenticated = writable<boolean>(false);
export const isLoading = writable<boolean>(true);
export const user = createUserStore();
export const error = createErrorStore();

export async function initializeAuth(): Promise<void> {
    if (!browser) return;

    try {
        const client = new Auth0Client(authConfig);
        auth0Client.set(client);

        if (window.location.search.includes("code=")) {
            await client.handleRedirectCallback();
            window.history.replaceState({}, document.title, window.location.pathname);
        }

        const isAuthenticatedResult = await client.isAuthenticated();
        isAuthenticated.set(isAuthenticatedResult);

        if (isAuthenticatedResult) {
            const userProfile = await client.getUser();
            if (userProfile) {
                // Add role based on email
                const isAdmin = userProfile.email === 'admin@example.com';
                user.set({
                    ...userProfile,
                    role: isAdmin ? 'admin' : 'user'
                });
            }
        }
    } catch (e) {
        if (e instanceof Error) {
            error.set(e);
        } else {
            error.set(new Error(String(e)));
        }
    } finally {
        isLoading.set(false);
    }
}

export async function login(): Promise<void> {
    if (!browser) return;

    try {
        const currentClient = get(auth0Client);
        if (!currentClient) {
            throw new Error('Auth0 client not initialized');
        }
        await currentClient.loginWithRedirect();
    } catch (e) {
        if (e instanceof Error) {
            error.set(e);
        } else {
            error.set(new Error(String(e)));
        }
    }
}

export async function logout(): Promise<void> {
    if (!browser) return;

    try {
        const currentClient = get(auth0Client);
        if (!currentClient) {
            throw new Error('Auth0 client not initialized');
        }
        await currentClient.logout({
            logoutParams: {
                returnTo: browser ? window.location.origin : 'http://localhost:5173'
            }
        });
    } catch (e) {
        if (e instanceof Error) {
            error.set(e);
        } else {
            error.set(new Error(String(e)));
        }
    }
}

export function getClient(): Auth0Client | null {
    return get(auth0Client);
}