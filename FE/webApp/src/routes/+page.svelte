<script lang="ts">
    import { isAuthenticated } from '$lib/auth/auth-store';
    import { goto } from '$app/navigation';

    function handleLoginClick() {
        goto('/login');
    }
</script>

<div class="login-container">
    <h1>Welcome</h1>
    {#if !$isAuthenticated}
        <button on:click={handleLoginClick}>Go to Login</button>
    {/if}
</div>

<style>
    .login-container {
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        min-height: 100vh;
    }
</style>