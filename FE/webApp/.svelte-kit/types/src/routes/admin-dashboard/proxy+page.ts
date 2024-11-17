// @ts-nocheck
import { redirect } from '@sveltejs/kit';
import type { PageLoad } from './$types';
import { get } from 'svelte/store';
import { isAuthenticated, user } from '$lib/auth/auth-store';
import { browser } from '$app/environment';

export const load = async () => {
    const currentUser = get(user);
    const isAuth = get(isAuthenticated);

    console.log('Admin guard check:', {
        isAuthenticated: isAuth,
        user: currentUser,
        role: currentUser?.role
    });

    if (!isAuth || currentUser?.role !== 'admin') {
        throw redirect(307, '/user-dashboard');
    }

    return {
        user: currentUser
    };
};;null as any as PageLoad;