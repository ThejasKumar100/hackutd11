<script lang="ts">
    import Header from './Header.svelte';
    import { user, logout } from '$lib/auth/auth-store';
    //import { getAllApplications } from '+page.ts'; this is a function btw
    // Need to have functionality like const [appData, setAppData] = useState();
    // setAppData(getAllApplications())
    import { goto } from '$app/navigation';

    async function handleLogout() {
        await logout();
        goto('/');
    }
</script>

<!-- <div class="admin-dashboard">
    <h1>Admin Dashboard</h1>
    {#if $user}
        <div class="user-info">
            <p>Welcome, Admin {$user.name}</p> -->
            <!-- <p>Email: {$user.email}</p>
            <p>Role: {$user.role}</p> -->
        <!-- </div>
        <button on:click={handleLogout}>Logout</button>
    {/if}
</div> -->


<Header />
<!-- <Header title="User Dashboard" /> -->


<div class="dashboard-container">
    <div class="dashboard-content">
        <div class="welcome-section">
            <h1>Welcome, {$user?.name || 'User'}</h1>
            <p class="subtitle">Manage incoming applications</p>
        </div>

        <div class="dashboard-grid">
            <div class="left-panel">
                <section class="account-info panel">
                    <h2>Account Information</h2>
                    <div class="info-grid">
                        <div class="info-item">
                            <span class="label">Email</span>
                            <span class="value">{$user?.email}</span>
                        </div>
                        <div class="info-item">
                            <span class="label">Account Status</span>
                            <span class="value status-active">Active</span>
                        </div>
                        <div class="info-item">
                            <span class="label">Member Since</span>
                            <span class="value">{new Date().toLocaleDateString()}</span>
                        </div>
                    </div>
                </section>


                <section class="applications panel">
                    <h2>Pending Applications</h2>
                    <div class="applications-list">
                        <!-- database -->
                         <!-- {#if $app}
                            {#each $app as application}
                                <div class="application-item">
                                    <span class="label">Application ID</span>
                                    <span class="value">{application.id}</span>
                                    <span class="label">Applicant</span>
                                    <span class="value">{application.applicant}</span>
                                    <span class="label">Date</span>
                                    <span class="value">{application.date}</span>
                                    <button class="action-button">View Application</button>
                                </div>
                            {/each}
                         {:else}
                         {/if} -->
                        <p class="no-applications">No pending applications</p>
                    </div>
                </section>
            </div>

            <div class="right-panel">
                <section class="quick-actions panel">
                    <h2>Quick Actions</h2>
                    <div class="actions-grid">
                        <button class="action-button">
                            <svg viewBox="0 0 24 24" width="24" height="24">
                                <path fill="currentColor" d="M11 17h2v-6h-2v6zm1-15C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm0 18c-4.41 0-8-3.59-8-8s3.59-8 8-8 8 3.59 8 8-3.59 8-8 8zM11 9h2V7h-2v2z"/>
                            </svg>
                            Account Details
                        </button>
                        <button class="action-button">
                            <svg viewBox="0 0 24 24" width="24" height="24">
                                <path fill="currentColor" d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm1.41 16.09V20h-2.67v-1.93c-1.71-.36-3.16-1.46-3.27-3.4h1.96c.1 1.05.82 1.87 2.65 1.87 1.96 0 2.4-.98 2.4-1.59 0-.83-.44-1.61-2.67-2.14-2.48-.6-4.18-1.62-4.18-3.67 0-1.72 1.39-2.84 3.11-3.21V4h2.67v1.95c1.86.45 2.79 1.86 2.85 3.39H14.3c-.05-1.11-.64-1.87-2.22-1.87-1.5 0-2.4.68-2.4 1.64 0 .84.65 1.39 2.67 1.91s4.18 1.39 4.18 3.91c-.01 1.83-1.38 2.83-3.12 3.16z"/>
                            </svg>
                            Payment History
                        </button>
                        <button class="action-button">
                            <svg viewBox="0 0 24 24" width="24" height="24">
                                <path fill="currentColor" d="M19 3h-4.18C14.4 1.84 13.3 1 12 1c-1.3 0-2.4.84-2.82 2H5c-1.1 0-2 .9-2 2v14c0 1.1.9 2 2 2h14c1.1 0 2-.9 2-2V5c0-1.1-.9-2-2-2zm-7 0c.55 0 1 .45 1 1s-.45 1-1 1-1-.45-1-1 .45-1 1-1zm2 14H7v-2h7v2zm3-4H7v-2h10v2zm0-4H7V7h10v2z"/>
                            </svg>
                            Documents
                        </button>
                        <button class="action-button">
                            <svg viewBox="0 0 24 24" width="24" height="24">
                                <path fill="currentColor" d="M12 1L3 5v6c0 5.55 3.84 10.74 9 12 5.16-1.26 9-6.45 9-12V5l-9-4zm0 10.99h7c-.53 4.12-3.28 7.79-7 8.94V12H5V6.3l7-3.11v8.8z"/>
                            </svg>
                            Security
                        </button>
                    </div>
                </section>
            </div>
        </div>
    </div>
</div>


<style>
    /* .admin-dashboard {
        padding: 2rem;
    }
    .user-info {
        margin: 1rem 0;
        padding: 1rem;
        background: #000000;
        border-radius: 4px;
    } */

    
    .dashboard-container {
        padding-top: 5rem;
        min-height: 100vh;
        background-color: rgb(24 24 27);
    }

    .dashboard-content {
        max-width: 1200px;
        margin: 0 auto;
        padding: 2rem;
    }

    .welcome-section {
        margin-bottom: 2rem;
    }

    h1 {
        color: white;
        font-size: 2rem;
        margin-bottom: 0.5rem;
    }

    .subtitle {
        color: rgb(161 161 170);
    }

    .dashboard-grid {
        display: grid;
        grid-template-columns: 2fr 1fr;
        gap: 2rem;
    }

    .panel {
        background-color: rgb(39 39 42);
        border-radius: 8px;
        padding: 1.5rem;
        margin-bottom: 1.5rem;
    }

    h2 {
        color: white;
        font-size: 1.25rem;
        margin-bottom: 1rem;
    }

    .info-grid {
        display: grid;
        gap: 1rem;
    }

    .info-item {
        display: flex;
        justify-content: space-between;
        align-items: center;
    }

    .label {
        color: rgb(161 161 170);
    }

    .value {
        color: white;
    }

    .status-active {
        color: #10B981;
    }

    /* .apply-button {
        width: 100%;
        padding: 1rem;
        background-color: #2563EB;
        color: white;
        border: none;
        border-radius: 6px;
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 0.5rem;
        cursor: pointer;
        transition: background-color 0.2s;
    } */

    /* .apply-button:hover {
        background-color: #1D4ED8;
    } */

    .no-applications {
        color: rgb(161 161 170);
        text-align: center;
        padding: 1rem;
    }

    .actions-grid {
        display: grid;
        grid-template-columns: repeat(2, 1fr);
        gap: 1rem;
    }

    .action-button {
        padding: 1rem;
        background-color: rgb(63 63 70);
        color: white;
        border: none;
        border-radius: 6px;
        display: flex;
        flex-direction: column;
        align-items: center;
        gap: 0.5rem;
        cursor: pointer;
        transition: background-color 0.2s;
    }

    .action-button:hover {
        background-color: rgb(82 82 91);
    }

    @media (max-width: 768px) {
        .dashboard-grid {
            grid-template-columns: 1fr;
        }

        .actions-grid {
            grid-template-columns: 1fr;
        }
    }
</style>