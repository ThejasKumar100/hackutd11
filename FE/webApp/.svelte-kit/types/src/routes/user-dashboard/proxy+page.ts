// @ts-nocheck
import { redirect } from '@sveltejs/kit';
import type { PageLoad } from './$types';
import { get } from 'svelte/store';
import { isAuthenticated, user } from '$lib/auth/auth-store';

export const load = async () => {
    const currentUser = get(user);
    const isAuth = get(isAuthenticated);

    console.log('User dashboard guard:', { isAuth, currentUser }); 

    if (!isAuth) {
        throw redirect(307, '/login');
    }

    return {
        user: currentUser
    };
};;null as any as PageLoad;