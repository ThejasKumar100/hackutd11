<script lang="ts">
    import { handleLogin, isAuthenticated, user } from '$lib/auth/auth-store';
    import { goto } from '$app/navigation';
    import { onMount } from 'svelte';
    import { browser } from '$app/environment';

    async function checkAndRedirect() {
        if ($isAuthenticated && $user) {
            console.log('User authenticated:', $user);
            const redirectPath = $user.role === 'admin' ? '/admin-dashboard' : '/user-dashboard';
            await goto(redirectPath);
        }
    }

    // checks for auth changes
    $: if ($isAuthenticated && $user && browser) {
        checkAndRedirect();
    }

    async function initiateLogin() {
        try {
            await handleLogin();
        } catch (error) {
            console.error('Login failed:', error);
        }
    }
</script>

<div class="login-container">
    <h1>Login</h1>

    <button class="learn-more" on:click={initiateLogin}>
        <span class="circle" aria-hidden="true">
            <span class="icon arrow"></span>
        </span>
        <span class="button-text">Log in</span>
    </button>

    <!-- <button on:click={initiateLogin}>Log in with Auth0</button> -->
    
    {#if import.meta.env.DEV}
        <div class="debug-info">
            <p>Authentication status: {$isAuthenticated ? 'Authenticated' : 'Not authenticated'}</p>
            {#if $user}
                <p>User email: {$user.email}</p>
                <p>User role: {$user.role}</p>
            {/if}
        </div>
    {/if}
</div>

<style>
    .login-container {
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        min-height: 100vh;
        gap: 1rem;
        color: white;
    }
    .debug-info {
        margin-top: 1rem;
        padding: 1rem;
        background: #f5f5f5;
        border-radius: 4px;
        color: black;
    }


        /* --------------------------- Button 1 */
button {
	position: relative;
	display: inline-block;
	cursor: pointer;
	outline: none;
	border: 0;
	vertical-align: middle;
	text-decoration: none;
	background: transparent;
	padding: 0;
	font-size: inherit;
	font-family: inherit;
   }
   
   button.learn-more {
	width: 12rem;
	height: auto;
   }
   
   button.learn-more .circle {
	transition: all 0.45s cubic-bezier(0.65, 0, 0.076, 1);
	position: relative;
	display: block;
	margin: 0;
	width: 3rem;
	height: 3rem;
	background: #282936;
	border-radius: 1.625rem;
   }
   
   button.learn-more .circle .icon {
	transition: all 0.45s cubic-bezier(0.65, 0, 0.076, 1);
	position: absolute;
	top: 0;
	bottom: 0;
	margin: auto;
	background: #fff;
   }
   
   button.learn-more .circle .icon.arrow {
	transition: all 0.45s cubic-bezier(0.65, 0, 0.076, 1);
	left: 0.625rem;
	width: 1.125rem;
	height: 0.125rem;
	background: none;
   }
   
   button.learn-more .circle .icon.arrow::before {
	position: absolute;
	content: "";
	top: -0.29rem;
	right: 0.0625rem;
	width: 0.625rem;
	height: 0.625rem;
	border-top: 0.125rem solid #fff;
	border-right: 0.125rem solid #fff;
	transform: rotate(45deg);
   }
   
   button.learn-more .button-text {
	transition: all 0.45s cubic-bezier(0.65, 0, 0.076, 1);
	position: absolute;
	top: 0;
	left: 0;
	right: 0;
	bottom: 0;
	padding: 0.75rem 0;
	margin: 0 0 0 1.85rem;
	color: #fff;
	font-weight: 700;
	line-height: 1.6;
	text-align: center;
	text-transform: uppercase;
   }
   
   button:hover .circle {
	width: 100%;
   }
   
   button:hover .circle .icon.arrow {
	background: #fff;
	transform: translate(1rem, 0);
   }
   
   button:hover .button-text {
	color: #fff;
   }
</style>