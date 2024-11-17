import { redirect } from '@sveltejs/kit';
import type { PageLoad } from './$types';
import { get } from 'svelte/store';
import { isAuthenticated, user } from '$lib/auth/auth-store';

export const load: PageLoad = async () => {
    const currentUser = get(user);
    const isAuth = get(isAuthenticated);

    // if (!isAuth) {
    //     throw redirect(307, '/login');
    // }

    return {
        user: currentUser
    };
};