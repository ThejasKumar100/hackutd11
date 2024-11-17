<script lang="ts">
    import { user, logout } from '$lib/auth/auth-store';
</script>

<div class="admin-dashboard">
    <h1>Admin Dashboard</h1>
    {#if $user}
        <p>Welcome, Admin {$user.name}</p>
        <div class="admin-controls">
            <h2>Admin Controls</h2>
            <!-- Add your admin-specific controls here -->
        </div>
    {/if}
    <button on:click={logout}>Logout</button>
</div>

<style>
    .admin-dashboard {
        padding: 2rem;
        max-width: 1200px;
        margin: 0 auto;
    }

    .admin-controls {
        margin-top: 2rem;
        padding: 1rem;
        border: 1px solid #ccc;
        border-radius: 4px;
    }
</style>