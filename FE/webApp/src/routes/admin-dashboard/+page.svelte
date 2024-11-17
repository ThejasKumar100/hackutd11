<script lang="ts">
    import Header from './Header.svelte';
    import { user } from '$lib/auth/auth-store';
    //import { getAllApplications } from '+page.ts'; this is a function btw
    // Need to have functionality like const [appData, setAppData] = useState();
    // setAppData(getAllApplications())
    import { goto } from '$app/navigation';
    import { onMount } from 'svelte';

    let applications = [
        {
            id: '1001',
            type: 'Credit Card',
            status: 'pending',
            submittedDate: new Date().toLocaleDateString()
        },
        {
            id: '1002',
            type: 'Credit Card',
            status: 'approved',
            submittedDate: new Date().toLocaleDateString()
        },
    ];

    function applyForCreditCard() {
        goto('/credit-card-applications');
    }

    function goToAccountDetails() {
        goto('/account-details');
    }
</script>

<Header />

<div class="dashboard-container">
    <div class="dashboard-content">
        <div class="welcome-section">
            <h1>Welcome, {$user?.name || 'User'}</h1>
            <p class="subtitle">Manage your account and applications</p>
        </div>

        <div class="dashboard-grid">
            <div class="left-panel">
                <!-- <section class="account-info panel">
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
                </section> -->

                <section class="services panel">
                    <h2>Services</h2>
                    <button class="apply-button" on:click={applyForCreditCard}>
                        <svg viewBox="0 0 24 24" width="24" height="24">
                            <path fill="currentColor" d="M20 4H4c-1.11 0-1.99.89-1.99 2L2 18c0 1.11.89 2 2 2h16c1.11 0 2-.89 2-2V6c0-1.11-.89-2-2-2zm0 14H4v-6h16v6zm0-10H4V6h16v2z"/>
                        </svg>
                        Apply for a Credit Card
                    </button>
                </section>

                <section class="services panel">
                    <h2>Services</h2>
                    <button class="apply-button" on:click={applyForCreditCard}>
                        <svg viewBox="0 0 24 24" width="24" height="24">
                            <path fill="currentColor" d="M20 4H4c-1.11 0-1.99.89-1.99 2L2 18c0 1.11.89 2 2 2h16c1.11 0 2-.89 2-2V6c0-1.11-.89-2-2-2zm0 14H4v-6h16v6zm0-10H4V6h16v2z"/>
                        </svg>
                        Apply for a Credit Card
                    </button>
                </section>

                <section class="applications panel">
                    <h2>Pending Applications</h2>
                    <div class="applications-list">
                        {#if applications.length === 0}
                            <p class="no-applications">No pending applications</p>
                        {:else}
                            <div class="applications-scroll">
                                <div class="application-cards">
                                    {#each applications as application}
                                        <div class="application-card">
                                            <div class="application-header">
                                                <span class="application-type">{application.type}</span>
                                                <span class="application-status {application.status}">
                                                    {application.status}
                                                </span>
                                            </div>
                                            <div class="application-details">
                                                <p class="application-date">
                                                    Submitted: {application.submittedDate}
                                                </p>
                                                <p class="application-id">ID: #{application.id}</p>
                                            </div>
                                        </div>
                                    {/each}
                                </div>
                            </div>

                        <!-- {/if} -->


                        <div class="card">
                            <div class="card2">

                                <div class="tileName"> <!-- First and Last name of the applicant -->
                                    First Last
                                </div>

                            </div>
                        </div>

                    </div>
                </section>
            </div>

            <div class="right-panel">
                <section class="quick-actions panel">
                    <h2>Quick Actions</h2>
                    <div class="actions-grid">
                        <button class="action-button" on:click={goToAccountDetails}>
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
                            Review Applications
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

    .tileName {
        position: relative;
        top: 15px;
        left: 15px;
        font-size: 20px;
        font-family: "Playfair Display", serif;
        color: white;
        font-weight: 600;
    }

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

    .apply-button {
        width: 100%;
        padding: 1rem;
        background-color: rgb(37, 99, 235);  
        color: white;
        border: none;
        border-radius: 6px;
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 0.5rem;
        cursor: pointer;
        transition: background-color 0.2s;
        font-size: 1rem;
        font-weight: 500;
    }

    .apply-button:hover {
        background-color: rgb(29, 78, 216);
    }

    .services {
        margin-bottom: 1.5rem;
    }

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

    /* ---------------------- Application Tiles */
    .card {
        width: 190px;
        height: 254px;
        background-image: linear-gradient(163deg, #00ff75 0%, #3700ff 100%);
        border-radius: 20px;
        transition: all .3s;
    }

    .card2 {
        width: 190px;
        height: 254px;
        background-color: #1a1a1a;
        border-radius: 15px;
        transition: all .2s;
    }

    .card2:hover {
        transform: scale(0.98);
        border-radius: 20px;
    }

    .card:hover {
        box-shadow: 0px 0px 30px 1px rgba(0, 255, 117, 0.30);
    }




    .applications-scroll {
        overflow-x: auto;
        padding: 0.5rem 0;
        margin: 0 -0.5rem;
    }

    .application-cards {
        display: flex;
        gap: 1rem;
        padding: 0 0.5rem;
        min-width: min-content;
    }

    .application-card {
        background-color: rgb(51 51 55);
        border-radius: 6px;
        padding: 1rem;
        min-width: 250px;
        border: 1px solid rgb(63 63 70);
    }

    .application-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 0.75rem;
    }

    .application-type {
        color: white;
        font-weight: 500;
    }

    .application-status {
        padding: 0.25rem 0.5rem;
        border-radius: 9999px;
        font-size: 0.75rem;
        font-weight: 500;
    }

    .application-status.pending {
        background-color: rgb(234 179 8 / 0.1);
        color: rgb(234 179 8);
    }

    .application-status.approved {
        background-color: rgb(34 197 94 / 0.1);
        color: rgb(34 197 94);
    }

    .application-details {
        display: flex;
        flex-direction: column;
        gap: 0.5rem;
    }

    .application-date,
    .application-id {
        color: rgb(161 161 170);
        font-size: 0.875rem;
    }

    /* Custom scrollbar styling */
    .applications-scroll::-webkit-scrollbar {
        height: 6px;
    }

    .applications-scroll::-webkit-scrollbar-track {
        background: rgb(39 39 42);
        border-radius: 3px;
    }

    .applications-scroll::-webkit-scrollbar-thumb {
        background: rgb(63 63 70);
        border-radius: 3px;
    }

    .applications-scroll::-webkit-scrollbar-thumb:hover {
        background: rgb(82 82 91);
    }

</style>