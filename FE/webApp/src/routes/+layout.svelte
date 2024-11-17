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

	
    $: if (!$isLoading && browser) {
        console.log('Auth state changed:', {
            isAuthenticated: $isAuthenticated,
            user: $user,
            currentPath: $page.url.pathname
        });

        if ($isAuthenticated && $user) {
            const isPublicRoute = ['/', '/login'].includes($page.url.pathname);
            if (isPublicRoute) {
                const redirectPath = $user.role === 'admin' ? '/admin-dashboard' : '/user-dashboard';
                goto(redirectPath);
            }
        }
    }
</script>

{#if $isLoading}
    <div>Loading...</div>
{:else}
    <slot />
{/if}