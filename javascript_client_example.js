// 🌐 JavaScript/Node.js API Client Example
// npm install node-fetch (for Node.js < 18) or use built-in fetch (Node.js 18+)

class TokenMarketClient {
    constructor(baseUrl = 'http://localhost:8000') {
        this.baseUrl = baseUrl;
        this.accessToken = null;
    }

    async register(email, password, username) {
        const response = await fetch(`${this.baseUrl}/auth/register`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ email, password, username })
        });
        return response.json();
    }

    async login(email, password) {
        const response = await fetch(`${this.baseUrl}/auth/login`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ email, password })
        });
        
        if (response.ok) {
            const data = await response.json();
            this.accessToken = data.access_token;
            return data;
        }
        return null;
    }

    async getProfile() {
        const response = await fetch(`${this.baseUrl}/profile`, {
            headers: { 'Authorization': `Bearer ${this.accessToken}` }
        });
        return response.json();
    }

    async getBalance() {
        const response = await fetch(`${this.baseUrl}/profile/balance`, {
            headers: { 'Authorization': `Bearer ${this.accessToken}` }
        });
        return response.json();
    }

    async getCollectibles() {
        const response = await fetch(`${this.baseUrl}/collectibles`);
        return response.json();
    }
}

// Usage Example:
async function example() {
    const client = new TokenMarketClient();
    
    // Register and login
    await client.register('js_user@example.com', 'password123', 'jsuser');
    const loginResult = await client.login('js_user@example.com', 'password123');
    
    if (loginResult) {
        // Access protected data
        const profile = await client.getProfile();
        const balance = await client.getBalance();
        console.log('Profile:', profile);
        console.log('Balance:', balance);
    }
    
    // Get public data
    const collectibles = await client.getCollectibles();
    console.log('Collectibles:', collectibles.length, 'items');
}
