<script lang="ts">
    import { onMount } from 'svelte';
    import { initializeAuth, isAuthenticated, isLoading, user } from '$lib/auth/auth-store';
    import { goto } from '$app/navigation';
    import { page } from '$app/stores';
    import { browser } from '$app/environment';

    onMount(() => {
        if (browser) {
            initializeAuth();
        }
    });

    // Add role-based route protection
    $: if (!$isLoading && $isAuthenticated && $user) {
        const currentPath = $page.url.pathname;
        if (currentPath.includes('admin-dashboard') && $user.role !== 'admin') {
            goto('/user-dashboard');
        }
    }
</script>

{#if $isLoading}
    <div>Loading...</div>
{:else}
    <slot />
{/if}