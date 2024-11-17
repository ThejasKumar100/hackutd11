<script lang="ts">
    import Header from '../user-dashboard/Header.svelte';
    import { goto } from '$app/navigation';

    // Mock user data (replace with actual data fetching logic)
    let user = {
        name: "John Doe",
        email: "john.doe@example.com",
        phone: "+1 234 567 8900",
        address: "123 Main St, Anytown, USA"
    };

    function handleSave() {
        // Implement save logic here
        console.log('Saving user details:', user);
        // After saving, you might want to show a success message or redirect
    }

    function handleCancel() {
        goto('/user-dashboard');
    }
</script>

<Header />

<div class="account-container">
    <div class="account-content">
        <div class="account-header">
            <h1>Account Details</h1>
            <p class="subtitle">Review and update your personal information</p>
        </div>

        <form class="account-form" on:submit|preventDefault={handleSave}>
            <div class="form-panel">
                <div class="form-group">
                    <label for="name">Full Name</label>
                    <input type="text" id="name" value={user.name} readonly>
                </div>

                <div class="form-group">
                    <label for="email">Email Address</label>
                    <input type="email" id="email" value={user.email} readonly>
                </div>

                <div class="form-group">
                    <label for="phone">Phone Number</label>
                    <input type="tel" id="phone" bind:value={user.phone}>
                </div>

                <div class="form-group">
                    <label for="address">Address</label>
                    <input type="text" id="address" bind:value={user.address}>
                </div>
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

<Header />

<div class="account-container">
    <div class="account-content">
        <div class="account-header">
            <h1>Account Details</h1>
            <p class="subtitle">Review and update your personal information</p>
        </div>

        <form class="account-form" on:submit|preventDefault={handleSave}>
            <div class="form-panel">
                <div class="form-group">
                    <label for="name">Full Name</label>
                    <input type="text" id="name" bind:value={user.name} required>
                    
                </div>

                <div class="form-group">
                    <label for="email">Email Address</label>
                    <input type="email" id="email" bind:value={user.email} required>
                </div>

                <div class="form-group">
                    <label for="phone">Phone Number</label>
                    <input type="tel" id="phone" bind:value={user.phone}>
                </div>

                <div class="form-group">
                    <label for="address">Address</label>
                    <input type="text" id="address" bind:value={user.address}>
                </div>
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
        padding-top: 5rem;
        min-height: 100vh;
        background-color: rgb(24 24 27);
    }

    .account-content {
        max-width: 600px;
        margin: 0 auto;
        padding: 2rem;
    }

    .account-header {
        margin-bottom: 3rem;
        text-align: center;
    }

    h1 {
        color: white;
        font-size: 2.5rem;
        margin-bottom: 0.75rem;
    }

    .subtitle {
        color: rgb(161 161 170);
        font-size: 1.1rem;
    }

    .form-panel {
        background-color: rgb(39 39 42);
        border-radius: 12px;
        padding: 2rem;
        margin-bottom: 2rem;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }

    .form-group {
        margin-bottom: 1.5rem;
    }

    label {
        display: block;
        color: white;
        margin-bottom: 0.5rem;
        font-size: 1rem;
        font-weight: 500;
    }

    input {
        width: 100%;
        padding: 0.75rem;
        border-radius: 6px;
        border: 1px solid rgb(63 63 70);
        background-color: rgb(51 51 55);
        color: white;
        font-size: 1rem;
        transition: border-color 0.2s, box-shadow 0.2s;
    }

    input[readonly] {
        background-color: rgb(45 45 48);
        cursor: not-allowed;
    }
    
    input:focus {
        outline: none;
        border-color: #3b82f6;
        box-shadow: 0 0 0 2px rgba(59, 130, 246, 0.3);
    }

    .button-group {
        display: flex;
        justify-content: flex-end;
        gap: 1rem;
    }

    .cancel-button, .save-button {
        padding: 0.75rem 1.5rem;
        border: none;
        border-radius: 6px;
        font-weight: 600;
        font-size: 1rem;
        cursor: pointer;
        transition: background-color 0.2s, transform 0.1s;
    }

    .cancel-button {
        background-color: rgb(63 63 70);
        color: white;
    }

    .cancel-button:hover {
        background-color: rgb(82 82 91);
        transform: translateY(-2px);
    }

    .save-button {
        background-color: #2563EB;
        color: white;
    }

    .save-button:hover {
        background-color: #1D4ED8;
        transform: translateY(-2px);
    }

    @media (max-width: 640px) {
        .account-content {
            padding: 1.5rem;
        }

        h1 {
            font-size: 2rem;
        }

        .subtitle {
            font-size: 1rem;
        }

        .form-panel {
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