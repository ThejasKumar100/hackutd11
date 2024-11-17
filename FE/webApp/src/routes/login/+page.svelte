<script lang="ts">
    import { handleLogin, isAuthenticated, user } from '$lib/auth/auth-store';
    import { goto } from '$app/navigation';
    import { onMount } from 'svelte';
    import { browser } from '$app/environment';

    let isLoggingIn = false;

// In your login/+page.svelte
async function checkAndRedirect() {
    console.log('Checking redirect conditions:', {
        isAuthenticated: $isAuthenticated,
        user: $user
    });
    
    if ($isAuthenticated && $user) {
        const redirectPath = $user.role === 'admin' ? '/admin-dashboard' : '/user-dashboard';
        console.log('Redirecting to:', redirectPath);
        await goto(redirectPath);
    }
}

    async function initiateLogin() {
        try {
            isLoggingIn = true;
            await handleLogin();
        } catch (error) {
            console.error('Login failed:', error);
        } finally {
            isLoggingIn = false;
        }
    }
</script>

<div class="login-container">
    <div class="login-card">
        <div class="auth0-logo">
            <svg viewBox="0 0 24 24" width="32" height="32">
                <path fill="currentColor" d="M21.98 7.448L19.62 0H4.347L2.02 7.448c-1.352 4.312.03 9.206 3.815 12.015L12 24l6.165-4.537c3.784-2.81 5.167-7.703 3.815-12.015zM12 6.634a2.978 2.978 0 110 5.956 2.978 2.978 0 010-5.956zm-6.921 9.198a7.026 7.026 0 01-.233-5.02l1.92-5.772h4.87a5.013 5.013 0 00-2.747 4.474c0 2.027 1.18 3.778 2.892 4.596a5.066 5.066 0 01-6.702 1.722zm13.842 0a5.066 5.066 0 01-6.702-1.722 5.013 5.013 0 002.892-4.596c0-1.97-1.121-3.68-2.747-4.474h4.87l1.92 5.773a7.026 7.026 0 01-.233 5.02z"/>
            </svg>
        </div>
        <h1>Welcome</h1>
        <p class="subtitle">Log in to HackUTD24 to continue</p>

        <button 
            class="login-button"
            on:click={initiateLogin}
            disabled={isLoggingIn}
        >
            <span class="button-content">
                {#if isLoggingIn}
                    <div class="spinner"></div>
                    Logging in...
                {:else}
                    <svg viewBox="0 0 24 24" width="18" height="18" class="google-icon">
                        <path fill="currentColor" d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm5.36 14.3c-.93-1.46-2.58-2.3-4.36-2.3s-3.43.84-4.36 2.3c-.84-1.27-1.36-2.79-1.36-4.3 0-4.42 3.58-8 8-8s8 3.58 8 8c0 1.51-.52 3.03-1.36 4.3z"/>
                    </svg>
                    Continue with Auth0
                {/if}
            </span>
        </button>

        {#if import.meta.env.DEV}
            <div class="debug-info">
                <p>Status: {$isAuthenticated ? 'Authenticated' : 'Not authenticated'}</p>
                {#if $user}
                    <p>Email: {$user.email}</p>
                    <p>Role: {$user.role}</p>
                {/if}
            </div>
        {/if}
    </div>
</div>

<style>
    .login-container {
        display: flex;
        align-items: center;
        justify-content: center;
        min-height: 100vh;
        padding: 1rem;
        background-color: rgb(24 24 27);
    }

    .login-card {
        background-color: rgb(39 39 42);
        padding: 2.5rem;
        border-radius: 8px;
        box-shadow: 0 4px 6px -1px rgb(0 0 0 / 0.1), 0 2px 4px -2px rgb(0 0 0 / 0.1);
        width: 100%;
        max-width: 400px;
        text-align: center;
    }

    .auth0-logo {
        margin-bottom: 1.5rem;
        color: #ffffff;
    }

    h1 {
        color: #ffffff;
        font-size: 1.5rem;
        font-weight: 600;
        margin: 0 0 0.5rem 0;
    }

    .subtitle {
        color: rgb(161 161 170);
        font-size: 0.875rem;
        margin-bottom: 2rem;
    }

    .login-button {
        width: 100%;
        padding: 0.75rem 1rem;
        background-color: rgb(63 63 70);
        color: #ffffff;
        border: none;
        border-radius: 6px;
        font-size: 0.875rem;
        font-weight: 500;
        cursor: pointer;
        transition: background-color 0.2s;
        display: flex;
        align-items: center;
        justify-content: center;
    }

    .login-button:hover {
        background-color: rgb(82 82 91);
    }

    .login-button:disabled {
        opacity: 0.7;
        cursor: not-allowed;
    }

    .button-content {
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }

    .google-icon {
        opacity: 0.9;
    }

    .spinner {
        width: 18px;
        height: 18px;
        border: 2px solid rgba(255, 255, 255, 0.3);
        border-radius: 50%;
        border-top-color: #ffffff;
        animation: spin 1s linear infinite;
    }

    .debug-info {
        margin-top: 2rem;
        padding: 1rem;
        background-color: rgb(63 63 70);
        border-radius: 6px;
        text-align: left;
        font-size: 0.875rem;
        color: rgb(161 161 170);
    }

    .debug-info p {
        margin: 0.25rem 0;
    }

    @keyframes spin {
        to {
            transform: rotate(360deg);
        }
    }

    @media (max-width: 480px) {
        .login-card {
            padding: 2rem 1.5rem;
        }
    }
</style>