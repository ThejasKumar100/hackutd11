<script lang="ts">
	import { user, logout } from '$lib/auth/auth-store';
	import { goto } from '$app/navigation';

	async function handleLogout() {
		await logout();
		goto('/');
	}
	export let title;
</script>

<header class="dashboard-header">
	<div class="header-content">
		<div class="logo">
			<span class="logo-icon">🏦</span>
			<span class="logo-text">HackUTD Bank</span>
		</div>

		<div class="user-controls">
			{#if $user}
				<span class="user-email">{$user.email}</span>
				<button class="logout-button" on:click={handleLogout}>
					<svg viewBox="0 0 24 24" width="18" height="18">
						<path
							fill="currentColor"
							d="M17 7l-1.41 1.41L18.17 11H8v2h10.17l-2.58 2.58L17 17l5-5zM4 5h8V3H4c-1.1 0-2 .9-2 2v14c0 1.1.9 2 2 2h8v-2H4V5z"
						/>
					</svg>
					Logout
				</button>
			{/if}
		</div>
	</div>
</header>

<style>
	.dashboard-header {
		background-color: rgb(39 39 42);
		padding: 1rem;
		box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
		position: fixed;
		top: 0;
		left: 0;
		right: 0;
		z-index: 100;
	}

	.header-content {
		max-width: 1200px;
		margin: 0 auto;
		display: flex;
		justify-content: space-between;
		align-items: center;
	}

	.logo {
		display: flex;
		align-items: center;
		gap: 0.5rem;
		font-size: 1.25rem;
		font-weight: 600;
		color: white;
	}

	.user-controls {
		display: flex;
		align-items: center;
		gap: 1rem;
	}

	.user-email {
		color: rgb(161 161 170);
	}

	.logout-button {
		display: flex;
		align-items: center;
		gap: 0.5rem;
		padding: 0.5rem 1rem;
		background-color: rgb(63 63 70);
		color: white;
		border: none;
		border-radius: 6px;
		cursor: pointer;
		transition: background-color 0.2s;
	}

	.logout-button:hover {
		background-color: rgb(82 82 91);
	}
</style>
