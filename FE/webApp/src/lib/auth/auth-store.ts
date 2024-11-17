import { writable, get, type Writable } from 'svelte/store';
import { Auth0Client, type User } from '@auth0/auth0-spa-js';
import { browser } from '$app/environment';
import { authConfig } from './auth-config';

// defines the user role types
type UserRole = 'admin' | 'user';

// defines the extendeduser types
interface ExtendedUser extends User {
    role?: UserRole;
}

// defines store types
type AuthStore = Writable<Auth0Client | null>;
type UserStore = Writable<ExtendedUser | null>;
type ErrorStore = Writable<Error | null>;

const ADMIN_EMAILS = ['nabil931260@gmail.com']; // admin emails here

const createAuthStore = (): AuthStore => {
    const { subscribe, set, update } = writable<Auth0Client | null>(null);
    return {
        subscribe,
        set,
        update
    };
};

const createUserStore = (): UserStore => {
    const { subscribe, set, update } = writable<ExtendedUser | null>(null);
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
                const isAdmin = ADMIN_EMAILS.includes(userProfile.email || '');
                const userWithRole: ExtendedUser = {
                    ...userProfile,
                    role: isAdmin ? 'admin' : 'user'
                };
                user.set(userWithRole);
            }
        }
    } catch (e) {
        error.set(e instanceof Error ? e : new Error(String(e)));
    } finally {
        isLoading.set(false);
    }
}

export async function handleLogin(): Promise<void> {
    if (!browser) return;

    try {
        const client = get(auth0Client);
        if (!client) {
            throw new Error('Auth0 client not initialized');
        }
        await client.loginWithRedirect();
    } catch (e) {
        error.set(e instanceof Error ? e : new Error(String(e)));
    }
}

export async function logout(): Promise<void> {
    if (!browser) return;

    try {
        const client = get(auth0Client);
        if (!client) {
            throw new Error('Auth0 client not initialized');
        }
        await client.logout({
            logoutParams: {
                returnTo: browser ? window.location.origin : 'http://localhost:5173'
            }
        });
    } catch (e) {
        error.set(e instanceof Error ? e : new Error(String(e)));
    }
}