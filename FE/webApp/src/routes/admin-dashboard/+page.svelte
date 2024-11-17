<script lang="ts">
    import AuthGuard from '$lib/components/AuthGuard.svelte';
    import { user, logout } from '$lib/auth/auth-store';
</script>

<AuthGuard>
    <div class="dashboard">
        <h1>Admin Dashboard</h1>
        {#if $user}
            <p>Welcome, Admin {$user.name}</p>
        {/if}
        <button on:click={logout}>Logout</button>
    </div>
</AuthGuard>

<style>
    .dashboard {
        padding: 2rem;
    }
</style>