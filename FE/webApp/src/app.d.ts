// See https://svelte.dev/docs/kit/types#app.d.ts
// for information about these interfaces
declare global {
	namespace App {
		// interface Error {}
		// interface Locals {}
		// interface PageData {}
		// interface PageState {}
		// interface Platform {}
	}
}

/// <reference types="@sveltejs/kit" />

declare module '$env/static/private' {
    export const MONGO_CLUSTER_CONNECTION_STRING: string;
    export const GMAIL_USER: string;
    export const GMAIL_APP_PASSWORD: string;
    export const SAMBANOVA_API_KEY: string;
}

declare namespace App {
    interface Locals {}
    interface PageData {}
    interface Platform {}
}

export {};
