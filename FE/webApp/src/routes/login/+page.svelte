<script lang="ts">
    import { login, isAuthenticated, user } from '$lib/auth/auth-store';
    import { goto } from '$app/navigation';

    $: if ($isAuthenticated && $user) {
        // Redirect based on role
        if ($user.role === 'admin') {
            goto('/admin-dashboard');
        } else {
            goto('/user-dashboard');
        }
    }

    async function handleLogin() {
        try {
            await login();
        } catch (error) {
            console.error('Login failed:', error);
        }
    }
</script>

<div class="login-container">
    <h1>Login</h1>
    <button on:click={handleLogin}>Log in with Auth0</button>
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
</style>