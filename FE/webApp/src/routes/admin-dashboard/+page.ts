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

export const getAllApplications = async() => {
    let uploadResponse: {status: string; message: string} | null = null;
    // Send the request to the server
    try {
        const response = await fetch('http://localhost:8000/all-apps/', {
            method: 'GET',
        });

        if (!response.ok) {
            return `Error retrieving applications: ${await response.text()}`;
        } else {
            const responseData = await response.json();
            console.log(responseData);
            return responseData;
        }
    } catch (error) {
        return `Error retrieving applications`;
    }
}

// export const load: PageLoad = async () => {
//     const currentUser = get(user);


//     return {
//         app: application
//     }
// };