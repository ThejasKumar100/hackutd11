<script lang="ts">
    import { onMount } from 'svelte';
    import { initializeAuth } from '$lib/auth/auth-store';
    import { browser } from '$app/environment';

    onMount(() => {
        if (browser) {
            initializeAuth();
        }
    });
</script>

<slot />