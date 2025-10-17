import type { Product, Recommendation } from '../types';

// The base URL for the Flask backend API
const API_BASE_URL = 'http://127.0.0.1:5000';

export async function getProducts(): Promise<Product[]> {
    console.log("[Frontend] Fetching products from backend...");
    try {
        const response = await fetch(`${API_BASE_URL}/api/products`);
        if (!response.ok) {
            const errorText = await response.text();
            throw new Error(`HTTP error! status: ${response.status}, message: ${errorText}`);
        }
        const products = await response.json();
        return products as Product[];
    } catch (error) {
        console.error("Failed to fetch products:", error);
        throw error; // Re-throw the error to be caught by the component
    }
}

export async function getRecommendations(
    userHistory: Product[],
    cart: Product[]
): Promise<Recommendation[]> {
    console.log("[Frontend] Fetching recommendations from backend...");
    try {
        const response = await fetch(`${API_BASE_URL}/api/recommendations`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ userHistory, cart })
        });
        if (!response.ok) {
            const errorText = await response.text();
            throw new Error(`HTTP error! status: ${response.status}, message: ${errorText}`);
        }
        const recommendations = await response.json();
        return recommendations as Recommendation[];
    } catch (error) {
        console.error("Failed to fetch recommendations:", error);
        // Return an empty array to prevent the app from crashing on recommendation failure
        return [];
    }
}