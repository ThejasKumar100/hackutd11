import { redirect } from '@sveltejs/kit';
import type { PageLoad } from './$types';
import { get } from 'svelte/store';
import { isAuthenticated, user } from '$lib/auth/auth-store';

export const load: PageLoad = async () => {
    const currentUser = get(user);
    const isAuth = get(isAuthenticated);

    if (!isAuth || currentUser?.role !== 'admin') {
        throw redirect(307, '/user-dashboard');
    }

    return {
        user: currentUser
    };
};

// export const load: PageLoad = async () => {
//     const currentUser = get(user);


//     return {
//         app: application
//     }
// };