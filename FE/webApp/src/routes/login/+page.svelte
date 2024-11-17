<script lang="ts">
	import Header from '../user-dashboard/Header.svelte';
	import { goto } from '$app/navigation';
	import { user } from '$lib/auth/auth-store';
	let userId: string | undefined = undefined;

	// Subscribe to the user store and update userId reactively
	$: if ($user) {
		userId = $user.sub; // Get user_id (sub field) from the user profile
	}

	interface FileState {
		idDocument: File | null;
		proofOfIncome: File[]; // Allow multiple files
	}

	let files: FileState = {
		idDocument: null,
		proofOfIncome: []
	};

	// Handle file changes
	function handleFileChange(event: Event, documentType: keyof FileState): void {
		const input = event.target as HTMLInputElement;
		if (input.files) {
			if (documentType === 'proofOfIncome') {
				files.proofOfIncome = Array.from(input.files); // Add all selected files
			} else {
				files[documentType] = input.files[0]; // Single file for ID document
			}
		}
	}

	// Handle form submission
	async function handleSubmit(): Promise<void> {
		const formData = new FormData();

		// Append user_id to formData if it's available
		if (userId) {
			formData.append('user_id', userId);
		}

		// Append ID Document
		if (files.idDocument) {
			formData.append('idDocument', files.idDocument);
		}

		// Append Proof of Income Files
		files.proofOfIncome.forEach((file, index) => {
			formData.append(`proofOfIncome[${index}]`, file);
		});

		try {
			const response = await fetch('http://localhost:8000/upload-images/', {
				method: 'POST',
				body: formData
			});

			if (response.ok) {
				console.log('Files successfully uploaded');
				goto('/user-dashboard');
			} else {
				console.error('Error uploading files:', await response.text());
			}
		} catch (error) {
			console.error('Submission failed:', error);
		}
	}

	// Handle cancel action
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
						<p class="description">
							Upload a valid government-issued ID (passport, driver's license)
						</p>
						<label class="upload-button">
							<input
								type="file"
								accept=".pdf,.jpg,.jpeg,.png"
								on:change={(e) => handleFileChange(e, 'idDocument')}
							/>
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
								multiple
								on:change={(e) => handleFileChange(e, 'proofOfIncome')}
							/>
							<span class="button-text">Upload Income Proof</span>
						</label>
					</div>
				</div>
			</div>

			<div class="button-group">
				<button type="button" class="cancel-button" on:click={handleCancel}> Cancel </button>
				<button type="submit" class="submit-button"> Submit Application </button>
			</div>
		</form>
	</div>
</div>

<style>
	.login-container {
		display: flex;
		align-items: center;
		justify-content: center;
		min-height: 100vh;
		padding: 1rem;
		background-color: rgb(24 24 27);
	}

	.login-card {
		background-color: rgb(39 39 42);
		padding: 2.5rem;
		border-radius: 8px;
		box-shadow:
			0 4px 6px -1px rgb(0 0 0 / 0.1),
			0 2px 4px -2px rgb(0 0 0 / 0.1);
		width: 100%;
		max-width: 400px;
		text-align: center;
	}

	.auth0-logo {
		margin-bottom: 1.5rem;
		color: #ffffff;
	}

	h1 {
		color: #ffffff;
		font-size: 1.5rem;
		font-weight: 600;
		margin: 0 0 0.5rem 0;
	}

	.subtitle {
		color: rgb(161 161 170);
		font-size: 0.875rem;
		margin-bottom: 2rem;
	}

	.login-button {
		width: 100%;
		padding: 0.75rem 1rem;
		background-color: rgb(63 63 70);
		color: #ffffff;
		border: none;
		border-radius: 6px;
		font-size: 0.875rem;
		font-weight: 500;
		cursor: pointer;
		transition: background-color 0.2s;
		display: flex;
		align-items: center;
		justify-content: center;
	}

	.login-button:hover {
		background-color: rgb(82 82 91);
	}

	.login-button:disabled {
		opacity: 0.7;
		cursor: not-allowed;
	}

	.button-content {
		display: flex;
		align-items: center;
		gap: 0.5rem;
	}

	.google-icon {
		opacity: 0.9;
	}

	.spinner {
		width: 18px;
		height: 18px;
		border: 2px solid rgba(255, 255, 255, 0.3);
		border-radius: 50%;
		border-top-color: #ffffff;
		animation: spin 1s linear infinite;
	}

	.debug-info {
		margin-top: 2rem;
		padding: 1rem;
		background-color: rgb(63 63 70);
		border-radius: 6px;
		text-align: left;
		font-size: 0.875rem;
		color: rgb(161 161 170);
	}

	.debug-info p {
		margin: 0.25rem 0;
	}

	@keyframes spin {
		to {
			transform: rotate(360deg);
		}
	}

	@media (max-width: 480px) {
		.login-card {
			padding: 2rem 1.5rem;
		}
	}
</style>
