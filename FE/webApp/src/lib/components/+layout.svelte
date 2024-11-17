<script lang="ts">
    import { onMount } from 'svelte';
    import { initializeAuth, isAuthenticated, isLoading, user } from '$lib/auth/auth-store';
    import { goto } from '$app/navigation';
    import { page } from '$app/stores';
    import { browser } from '$app/environment';

    let initializationAttempted = false;

    onMount(async () => {
        if (browser && !initializationAttempted) {
            initializationAttempted = true;
            try {
                await initializeAuth();
            } catch (error) {
                console.error('Auth initialization error:', error);
            }
        }
    });

    $: if (browser && !$isLoading && $isAuthenticated && $user) {
        const publicRoutes = ['/', '/login'];
        const currentPath = $page.url.pathname;
        
        if (publicRoutes.includes(currentPath)) {
            const redirectPath = $user.role === 'admin' ? '/admin-dashboard' : '/user-dashboard';
            console.log('Redirecting to:', redirectPath);
            goto(redirectPath);
        }
    }
</script>

<div class="app-container">
    {#if $isLoading}
        <div class="loading-screen">
            <div class="loading-spinner"></div>
            <p class="loading-text">Loading...</p>
        </div>
    {:else}
        <main class="main-content">
            <slot />
        </main>
    {/if}
</div>

<style>
    :global(body) {
        margin: 0;
        padding: 0;
        background-color: rgb(24 24 27);
        color: #fff;
        font-family: system-ui, -apple-system, sans-serif;
    }

    .app-container {
        min-height: 100vh;
        display: flex;
        flex-direction: column;
    }

    .loading-screen {
        position: fixed;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        background-color: rgb(24 24 27);
        z-index: 50;
    }

    .loading-spinner {
        width: 40px;
        height: 40px;
        border: 3px solid rgba(255, 255, 255, 0.1);
        border-radius: 50%;
        border-top-color: #fff;
        animation: spin 1s ease-in-out infinite;
        margin-bottom: 1rem;
    }

    .loading-text {
        color: #fff;
        font-size: 1.125rem;
        font-weight: 500;
    }

    .main-content {
        flex: 1;
        width: 100%;
        max-width: 1200px;
        margin: 0 auto;
        padding: 1rem;
    }

    @keyframes spin {
        to {
            transform: rotate(360deg);
        }
    }

    @media (max-width: 768px) {
        .main-content {
            padding: 1rem 0.5rem;
        }
    }
</style>