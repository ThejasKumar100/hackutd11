// src/lib/models/creditApplication.ts
import type { ObjectId } from 'mongodb';

export interface CreditApplication {
    _id?: ObjectId;
    userId: string;
    email: string;
    status: ApplicationStatus;
    documents: ApplicationDocuments;
    createdAt: Date;
}

export type ApplicationStatus = 'pending' | 'approved' | 'rejected';

export interface ApplicationDocuments {
    idDocument: string;
    proofOfIncome: string;
}

// If you need to type the file uploads
export interface FileState {
    idDocument: File | null;
    proofOfIncome: File | null;
}

// API response types
export interface ApplicationResponse {
    success: boolean;
    applications?: CreditApplication[];
    error?: string;
}

export interface SubmitApplicationResponse {
    success: boolean;
    id?: string;
    error?: string;
}