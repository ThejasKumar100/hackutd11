<script lang="ts">
    import { isAuthenticated, isLoading } from '$lib/auth/auth-store';
    import { goto } from '$app/navigation';

    $: if (!$isLoading && !$isAuthenticated) {
        goto('/');
    }
</script>

{#if $isLoading}
    <div>Loading...</div>
{:else if $isAuthenticated}
    <slot />
{/if}