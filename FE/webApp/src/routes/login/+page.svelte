<script lang="ts">
    import { handleLogin, isAuthenticated, user } from '$lib/auth/auth-store';
    import { goto } from '$app/navigation';
    import { onMount } from 'svelte';
    import { browser } from '$app/environment';

    async function checkAndRedirect() {
        if ($isAuthenticated && $user) {
            console.log('User authenticated:', $user);
            const redirectPath = $user.role === 'admin' ? '/admin-dashboard' : '/user-dashboard';
            await goto(redirectPath);
        }
    }

    // checks for auth changes
    $: if ($isAuthenticated && $user && browser) {
        checkAndRedirect();
    }

    async function initiateLogin() {
        try {
            await handleLogin();
        } catch (error) {
            console.error('Login failed:', error);
        }
    }
</script>

<div class="login-container">
    <h1>Login</h1>
    <button on:click={initiateLogin}>Log in with Auth0</button>
    
    {#if import.meta.env.DEV}
        <div class="debug-info">
            <p>Authentication status: {$isAuthenticated ? 'Authenticated' : 'Not authenticated'}</p>
            {#if $user}
                <p>User email: {$user.email}</p>
                <p>User role: {$user.role}</p>
            {/if}
        </div>
    {/if}
</div>

<style>
    .login-container {
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        min-height: 100vh;
        gap: 1rem;
    }
    .debug-info {
        margin-top: 1rem;
        padding: 1rem;
        background: #f5f5f5;
        border-radius: 4px;
    }
</style>