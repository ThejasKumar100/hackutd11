<script lang="ts">
    import AuthGuard from '$lib/components/AuthGuard.svelte';
    import { user, logout } from '$lib/auth/auth-store';
    import { browser } from '$app/environment';
    import { redirect } from '@sveltejs/kit';
    import { get } from 'svelte/store';
    import { isAuthenticated } from '$lib/auth/auth-store';
</script>

<AuthGuard>
    <div class="dashboard">
        <h1>User Dashboard</h1>
        {#if $user}
            <p>Welcome, {$user.name}</p>
        {/if}
        <button on:click={logout}>Logout</button>
    </div>
</AuthGuard>

<style>
    .dashboard {
        padding: 2rem;
    }
</style>