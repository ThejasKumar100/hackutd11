<script lang="ts">
	import Header from '../user-dashboard/Header.svelte';
	import { goto } from '$app/navigation';
	import { user } from '$lib/auth/auth-store';
	let userId: string | undefined = undefined;

	$: {
		if ($user) {
			userId = $user.sub; // Get user_id (sub field) from the user profile
		}
	}

	interface FileState {
		idDocument: File | null;
		proofOfIncome: File[]; // Allow multiple files
	}

	let files: FileState = {
		idDocument: null,
		proofOfIncome: []
	};

	let uploading = false;
	let uploadResponse: { status: string; message: string } | null = null;

	function handleFileChange(event: Event, documentType: keyof FileState): void {
		const input = event.target as HTMLInputElement;
		if (input.files) {
			if (documentType === 'proofOfIncome') {
				files.proofOfIncome.push(...Array.from(input.files));
				console.log(files.proofOfIncome);
			} else {
				files[documentType] = input.files[0];
				console.log(files[documentType]);
			}
		}
	}

	const handleSubmit = async () => {
		const formData = new FormData();
		uploading = true;
		uploadResponse = null;

		// Append user_id
		formData.append('user_id', userId);

		// Append the idDocument (if exists)
		if (files.idDocument) {
			formData.append('files', files.idDocument); // Add as a single file under "files"
		}

		// Append all files in proofOfIncome
		files.proofOfIncome.forEach((file) => {
			formData.append('files', file); // Add each file to the "files" field
		});

		// Send the request to the server
		try {
			const response = await fetch('http://localhost:8000/upload-images/', {
				method: 'POST',
				body: formData
			});

			if (!response.ok) {
				uploadResponse = {
					status: 'error',
					message: `Error uploading files: ${await response.text()}`
				};
			} else {
				const responseData = await response.json();
				uploadResponse = {
					status: 'success',
					message: 'Files uploaded successfully!'
				};
				// Clear the files after successful upload
				files = { idDocument: null, proofOfIncome: [] };
			}
		} catch (error) {
			uploadResponse = {
				status: 'error',
				message: `Error sending request: ${error.message}`
			};
		} finally {
			uploading = false;
		}
	};

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
						{#if files.idDocument}
							<p class="file-name">{files.idDocument.name}</p>
						{/if}
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
						{#if files.proofOfIncome.length > 0}
							<ul class="file-list">
								{#each files.proofOfIncome as file}
									<li>{file.name}</li>
								{/each}
							</ul>
						{/if}
					</div>
				</div>
			</div>

			<div class="button-group">
				<button type="button" class="cancel-button" on:click={handleCancel}> Cancel </button>
				<button type="submit" class="submit-button" disabled={uploading}>
					{#if uploading}
						<span class="loading-spinner"></span> Uploading...
					{:else}
						Submit Application
					{/if}
				</button>
			</div>
		</form>
	</div>
</div>

{#if uploadResponse}
	<div class="popup">
		<div class="popup-content">
			<p>{uploadResponse.message}</p>
			<button on:click={() => (uploadResponse = null)}>Close</button>
		</div>
	</div>
{/if}

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
		transition:
			background-color 0.2s,
			transform 0.1s;
		font-size: 1rem;
		font-weight: 500;
	}

	.upload-button:hover .button-text {
		background-color: rgb(82 82 91);
		transform: translateY(-2px);
	}

	.file-list {
		color: white;
		font-size: 0.9rem;
		list-style-type: none;
		padding-left: 0;
		margin-top: 1rem;
	}

	.file-name {
		color: white;
		font-size: 0.9rem;
		text-align: center;
	}

	.button-group {
		display: flex;
		justify-content: flex-end;
		gap: 1.5rem;
		margin-top: 3rem;
	}

	.cancel-button,
	.submit-button {
		padding: 1rem 2rem;
		border: none;
		border-radius: 8px;
		font-weight: 600;
		font-size: 1rem;
		cursor: pointer;
		transition:
			background-color 0.2s,
			transform 0.1s;
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
		background-color: #2563eb;
		color: white;
	}

	.submit-button:hover {
		background-color: #1d4ed8;
		transform: translateY(-2px);
	}

	.popup {
		position: fixed;
		top: 0;
		left: 0;
		right: 0;
		bottom: 0;
		background-color: rgba(0, 0, 0, 0.5);
		display: flex;
		justify-content: center;
		align-items: center;
	}
</style>
