export interface UserInfo {
    // Basic Info
    name: {
        firstName: string;
        lastName: string;
        middleName?: string;  // Optional field
    };
    email: string;
    
    // Contact Info
    phone: {
        primary: string;
        secondary?: string;  // Optional field
    };
    
    // Address Info
    address: {
        street: string;
        unit?: string;      // Optional field
        city: string;
        state: string;
        zipCode: string;
        country: string;
    };
    
    // Optional metadata
    createdAt?: Date;
    updatedAt?: Date;
}

// Helper type for form submission
export interface UserInfoFormData {
    firstName: string;
    lastName: string;
    middleName?: string;
    email: string;
    phoneNumber: string;
    alternatePhone?: string;
    street: string;
    unit?: string;
    city: string;
    state: string;
    zipCode: string;
    country: string;
}

// Validation type
export interface UserInfoValidation {
    isValid: boolean;
    errors: {
        name?: string;
        email?: string;
        phone?: string;
        address?: string;
    };
}