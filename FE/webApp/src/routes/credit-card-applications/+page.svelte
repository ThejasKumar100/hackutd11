<script lang="ts">
    import Header from '../user-dashboard/Header.svelte';
    import { goto } from '$app/navigation';

    interface FileState {
        idDocument: File | null;
        proofOfIncome: File | null;
    }

    let files: FileState = {
        idDocument: null,
        proofOfIncome: null,
    };

    function handleFileChange(event: Event, documentType: keyof FileState): void {
        const input = event.target as HTMLInputElement;
        if (input.files && input.files[0]) {
            files[documentType] = input.files[0];
        }
    }

    async function handleSubmit(): Promise<void> {
        console.log('Submitting files:', files);
        goto('/user-dashboard');
    }

    function handleCancel(): void {
        goto('/user-dashboard');
    }
</script>

<Header />

<div class="application-container">
    <div class="application-content">
        <div class="application-header">
            <h1>Credit Card Application</h1>
            <p class="subtitle">Please provide sufficient documents to process your application</p>
        </div>

        <form class="application-form" on:submit|preventDefault={handleSubmit}>
            <div class="document-section">
                <h2>Required Documents</h2>
                
                <div class="document-grid">
                    <div class="document-upload panel">
                        <h3>Government ID</h3>
                        <p class="description">Upload a valid government-issued ID (passport, driver's license)</p>
                        <label class="upload-button">
                            <input 
                                type="file" 
                                accept=".pdf,.jpg,.jpeg,.png" 
                                on:change={(e) => handleFileChange(e, 'idDocument')}
                            >
                            <span class="button-text">Upload ID Document</span>
                        </label>
                    </div>

                    <div class="document-upload panel">
                        <h3>Proof of Income</h3>
                        <p class="description">Bills, Rent Invoices, Property Deeds, etc</p>
                        <label class="upload-button">
                            <input 
                                type="file" 
                                accept=".pdf,.jpg,.jpeg,.png" 
                                on:change={(e) => handleFileChange(e, 'proofOfIncome')}
                            >
                            <span class="button-text">Upload Income Proof</span>
                        </label>
                    </div>
                </div>
            </div>

            <div class="button-group">
                <button type="button" class="cancel-button" on:click={handleCancel}>
                    Cancel
                </button>
                <button type="submit" class="submit-button">
                    Submit Application
                </button>
            </div>
        </form>
    </div>
</div>

<style>
    .application-container {
        padding-top: 5rem;
        min-height: 100vh;
        background-color: rgb(24 24 27);
    }

    .application-content {
        max-width: 800px;
        margin: 0 auto;
        padding: 2rem;
    }

    .application-header {
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

    .document-section h2 {
        color: white;
        font-size: 1.8rem;
        margin-bottom: 1.5rem;
    }

    .document-grid {
        display: grid;
        grid-template-columns: 1fr;
        gap: 2rem;
        margin-bottom: 3rem;
    }

    .panel {
        background-color: rgb(39 39 42);
        border-radius: 12px;
        padding: 2rem;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }

    h3 {
        color: white;
        font-size: 1.4rem;
        margin-bottom: 1rem;
    }

    .description {
        color: rgb(161 161 170);
        font-size: 1rem;
        margin-bottom: 1.5rem;
    }

    .upload-button {
        display: block;
        cursor: pointer;
    }

    .upload-button input {
        display: none;
    }

    .button-text {
        display: block;
        padding: 1rem 1.5rem;
        background-color: rgb(63 63 70);
        color: white;
        border-radius: 8px;
        text-align: center;
        transition: background-color 0.2s, transform 0.1s;
        font-size: 1rem;
        font-weight: 500;
    }

    .upload-button:hover .button-text {
        background-color: rgb(82 82 91);
        transform: translateY(-2px);
    }

    .button-group {
        display: flex;
        justify-content: flex-end;
        gap: 1.5rem;
        margin-top: 3rem;
    }

    .cancel-button, .submit-button {
        padding: 1rem 2rem;
        border: none;
        border-radius: 8px;
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

    .submit-button {
        background-color: #2563EB;
        color: white;
    }

    .submit-button:hover {
        background-color: #1D4ED8;
        transform: translateY(-2px);
    }

    @media (max-width: 768px) {
        .application-content {
            padding: 1.5rem;
        }

        h1 {
            font-size: 2rem;
        }

        .subtitle {
            font-size: 1rem;
        }

        .document-section h2 {
            font-size: 1.5rem;
        }

        .panel {
            padding: 1.5rem;
        }

        h3 {
            font-size: 1.2rem;
        }

        .button-text, .cancel-button, .submit-button {
            font-size: 0.9rem;
            padding: 0.75rem 1.25rem;
        }
    }
</style>