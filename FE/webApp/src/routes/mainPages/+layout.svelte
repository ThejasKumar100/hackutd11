<script lang="ts">
    // import type { Snippet } from 'svelte';
    // import type { LayoutData } from './$types';

    
    
    // let { data, children }: { data: LayoutData, children: Snippet } = $props();


</script>

<div class="section1" color="black">
    <p>This is Test Text!</p>
</div>

<div class="section2" color="black">
    <p>This is Test Text!</p>
</div>


<style>

    .section1 {

        position: relative;
        top: 10vh;
        left: 2vw;
        background-color: #f1f1f1;
        width: 36vw;
        height: 85vh;

        /* display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        min-height: 100vh; */
        gap: 1rem;
        color: white;
    }

    .section2 {

        position: relative;
        top: -77vh;
        left: 39vw;
        background-color: #f1f1f1;
        width: 59vw;
        height: 85vh;

        /* display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        min-height: 100vh; */
        gap: 1rem;
        color: white;
    }

</style>

<!-- {@render children()} -->