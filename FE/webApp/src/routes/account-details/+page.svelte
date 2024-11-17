<script lang="ts">
    import Header from '../user-dashboard/Header.svelte';
    import { goto } from '$app/navigation';
    import { user } from '$lib/auth/auth-store';

    let userInfo = {
        name: $user?.name || '',
        email: $user?.email || '',
        phone: '',
        address: ''
    };

    function handleSave(event: Event) {
        event.preventDefault();
        console.log('Saving user info:', userInfo);
        goto('/user-dashboard');
    }

    function handleCancel() {
        goto('/user-dashboard');
    }
</script>

<div class="account-container">
    <div class="account-content">
        <div class="account-header">
            <h1>Account Details</h1>
            <p class="subtitle">Review and update your personal information</p>
        </div>

        <form class="account-form" on:submit|preventDefault={handleSave}>
            <div class="form-group">
                <label for="name">Full Name</label>
                <input 
                    type="text" 
                    id="name" 
                    bind:value={userInfo.name}
                    readonly
                    class="input-dark"
                >
            </div>

            <div class="form-group">
                <label for="email">Email Address</label>
                <input 
                    type="email" 
                    id="email" 
                    bind:value={userInfo.email}
                    readonly
                    class="input-dark"
                >
            </div>

            <div class="form-group">
                <label for="phone">Phone Number</label>
                <input 
                    type="tel" 
                    id="phone" 
                    bind:value={userInfo.phone}
                    placeholder="Enter your phone number"
                    class="input-dark"
                >
            </div>

            <div class="form-group">
                <label for="address">Address</label>
                <input 
                    type="text" 
                    id="address" 
                    bind:value={userInfo.address}
                    placeholder="Enter your address"
                    class="input-dark"
                >
            </div>

            <div class="button-group">
                <button type="button" class="cancel-button" on:click={handleCancel}>
                    Cancel
                </button>
                <button type="submit" class="save-button">
                    Save Changes
                </button>
            </div>
        </form>
    </div>
</div>

<style>
    .account-container {
        min-height: 100vh;
        background-color: rgb(24 24 27);
        display: flex;
        align-items: center;
        justify-content: center;
        padding: 2rem;
    }

    .account-content {
        width: 100%;
        max-width: 480px;
        background-color: rgb(32 32 35);
        border-radius: 12px;
        padding: 2rem;
    }

    .account-header {
        text-align: center;
        margin-bottom: 2rem;
    }

    h1 {
        color: white;
        font-size: 2rem;
        font-weight: 600;
        margin-bottom: 0.5rem;
    }

    .subtitle {
        color: rgb(161 161 170);
        font-size: 0.875rem;
    }

    .form-group {
        margin-bottom: 1.25rem;
    }

    label {
        display: block;
        color: rgb(161 161 170);
        font-size: 0.875rem;
        margin-bottom: 0.5rem;
    }

    .input-dark {
        width: 100%;
        padding: 0.75rem;
        background-color: rgb(24 24 27);
        border: 1px solid rgb(63 63 70);
        border-radius: 6px;
        color: white;
        font-size: 0.875rem;
        transition: border-color 0.2s;
    }

    .input-dark:focus {
        outline: none;
        border-color: rgb(37 99 235);
    }

    .input-dark[readonly] {
        background-color: rgb(45 45 48);
        cursor: not-allowed;
    }

    .input-dark::placeholder {
        color: rgb(161 161 170);
    }

    .button-group {
        display: flex;
        justify-content: flex-end;
        gap: 0.75rem;
        margin-top: 2rem;
    }

    .cancel-button, .save-button {
        padding: 0.75rem 1.5rem;
        border: none;
        border-radius: 6px;
        font-size: 0.875rem;
        font-weight: 500;
        cursor: pointer;
        transition: background-color 0.2s;
    }

    .cancel-button {
        background-color: rgb(63 63 70);
        color: white;
    }

    .cancel-button:hover {
        background-color: rgb(82 82 91);
    }

    .save-button {
        background-color: rgb(37 99 235);
        color: white;
    }

    .save-button:hover {
        background-color: rgb(29 78 216);
    }

    @media (max-width: 640px) {
        .account-container {
            padding: 1rem;
        }

        .account-content {
            padding: 1.5rem;
        }

        .button-group {
            flex-direction: column;
        }

        .cancel-button, .save-button {
            width: 100%;
        }
    }
</style>