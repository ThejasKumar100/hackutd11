import { writable, get, type Writable } from 'svelte/store';
import { Auth0Client, type User, type LogoutOptions } from '@auth0/auth0-spa-js';
import { authConfig } from './auth-config';

// Define types
type AuthStore = Writable<Auth0Client | null>;
type UserStore = Writable<User | null>;
type ErrorStore = Writable<Error | null>;

// Initialize stores with proper types
const createAuthStore = (): AuthStore => {
    const { subscribe, set, update } = writable<Auth0Client | null>(null);
    return {
        subscribe,
        set: (client: Auth0Client | null) => set(client),
        update
    };
};

const createUserStore = (): UserStore => {
    const { subscribe, set, update } = writable<User | null>(null);
    return {
        subscribe,
        set: (userData: User | null) => set(userData),
        update
    };
};

const createErrorStore = (): ErrorStore => {
    const { subscribe, set, update } = writable<Error | null>(null);
    return {
        subscribe,
        set: (error: Error | null) => set(error),
        update
    };
};

export const auth0Client = createAuthStore();
export const isAuthenticated = writable<boolean>(false);
export const isLoading = writable<boolean>(true);
export const user = createUserStore();
export const error = createErrorStore();

export async function initializeAuth(): Promise<void> {
    try {
        const client = new Auth0Client(authConfig);
        auth0Client.set(client);

        // Checks if the user was redirected after they login
        if (window.location.search.includes("code=")) {
            await client.handleRedirectCallback();
            window.history.replaceState({}, document.title, window.location.pathname);
        }

        const isAuthenticatedResult = await client.isAuthenticated();
        isAuthenticated.set(isAuthenticatedResult);

        if (isAuthenticatedResult) {
            const userProfile = await client.getUser();
            if (userProfile) {
                user.set(userProfile);
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
    try {
        const currentClient = get(auth0Client);
        if (!currentClient) {
            throw new Error('Auth0 client not initialized');
        }
        const logoutOptions: LogoutOptions = {
            logoutParams: {
                returnTo: window.location.origin
            }
        };
        await currentClient.logout(logoutOptions);
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