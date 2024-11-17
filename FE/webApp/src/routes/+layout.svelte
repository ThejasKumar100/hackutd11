<script lang="ts">
    import { onMount } from 'svelte';
    import { initializeAuth, isAuthenticated, isLoading, user } from '$lib/auth/auth-store';
    import { goto } from '$app/navigation';
    import { page } from '$app/stores';
    import { browser } from '$app/environment';

    onMount(async () => {
        if (browser) {
            try {
                await initializeAuth();
            } catch (error) {
                console.error('Auth initialization error:', error);
            }
        }
    });

    // Handle authenticated routes
    $: if (browser && !$isLoading && $isAuthenticated && $user) {
        const publicRoutes = ['/', '/login'];
        if (publicRoutes.includes($page.url.pathname)) {
            const redirectPath = $user.role === 'admin' ? '/admin-dashboard' : '/user-dashboard';
            goto(redirectPath);
        }
    }
</script>

<slot />

<div class="section1" color="black">

</div>

<div class="section2" color="black">

</div>


<style>

    .section1 {

        position: relative;
        top: 10vh;
        left: 2vw;
        background-color: #f1f1f1;
        width: 36vw;
        height: 85vh;

        /* display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        min-height: 100vh; */
        gap: 1rem;
        border-radius: 4vh;
        color: white;
    }

    .section2 {

        position: relative;
        top: -75vh;
        left: 39vw;
        background-color: #f1f1f1;
        width: 59vw;
        height: 85vh;

        /* display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        min-height: 100vh; */
        gap: 1rem;
        border-radius: 4vh;
        color: white;
    }

</style>

<!-- {@render children()} -->