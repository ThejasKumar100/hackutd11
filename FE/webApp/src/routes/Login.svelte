<script lang="ts">
    import { login, isAuthenticated, user } from '$lib/auth/auth-store';
    import { goto } from '$app/navigation';

    $: if ($isAuthenticated && $user) {
        if ($user.email === 'admin@example.com') {
            goto('/admin-dashboard');
        } else {
            goto('/user-dashboard');
        }
    }
</script>

<div class="login-container">
    <h1>Welcome</h1>
    <button on:click={login}>Log In</button>
</div>

<style>
    .login-container {
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        height: 100vh;
    }
</style>