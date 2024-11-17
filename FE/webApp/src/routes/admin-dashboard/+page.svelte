<script lang="ts">
    import { user, logout } from '$lib/auth/auth-store';
    import { goto } from '$app/navigation';

    async function handleLogout() {
        await logout();
        goto('/');
    }
</script>

<div class="admin-dashboard">
    <h1>Admin Dashboard</h1>
    {#if $user}
        <div class="user-info">
            <p>Welcome, Admin {$user.name}</p>
            <!-- <p>Email: {$user.email}</p>
            <p>Role: {$user.role}</p> -->
        </div>
        <button on:click={handleLogout}>Logout</button>
    {/if}
</div>

<style>
    .admin-dashboard {
        padding: 2rem;
    }
    .user-info {
        margin: 1rem 0;
        padding: 1rem;
        background: #000000;
        border-radius: 4px;
    }
</style>