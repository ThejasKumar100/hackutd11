import type { Auth0ClientOptions } from '@auth0/auth0-spa-js';

export const authConfig: Auth0ClientOptions = {
    domain: 'dev-d0438ykyws2br7op.us.auth0.com',
    clientId: 'mUWSaw5J8fOgAtCuIwHMBIFBJwSIGkmV',
    authorizationParams: {
        redirect_uri: window.location.origin
    }
};