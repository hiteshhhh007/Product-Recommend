import React, { useState, useEffect, useCallback } from 'react';
import Header from './components/Header';
import ProductGrid from './components/ProductGrid';
import ShoppingCart from './components/ShoppingCart';
import Recommendations from './components/Recommendations';
import Toast from './components/Toast';
import Pagination from './components/Pagination';
import { getProducts, getRecommendations } from './services/apiService';
import type { Product, Recommendation } from './types';

const App: React.FC = () => {
    const [products, setProducts] = useState<Product[]>([]);
    const [isProductsLoading, setIsProductsLoading] = useState<boolean>(true);
    const [userHistory, setUserHistory] = useState<Product[]>([]);
    const [cart, setCart] = useState<Product[]>([]);
    const [recommendations, setRecommendations] = useState<Recommendation[]>([]);
    const [isLoading, setIsLoading] = useState<boolean>(false);
    const [error, setError] = useState<string | null>(null);
    const [toastMessage, setToastMessage] = useState<string>('');
    const [showToast, setShowToast] = useState<boolean>(false);
    
    // Pagination state
    const [currentPage, setCurrentPage] = useState<number>(1);
    const productsPerPage = 9;

    // Fetch products on initial load from the backend
    useEffect(() => {
        const loadProducts = async () => {
            try {
                const fetchedProducts = await getProducts();
                setProducts(fetchedProducts);
            } catch (err) {
                setError("Failed to load products.");
                console.error(err);
            } finally {
                setIsProductsLoading(false);
            }
        };
        loadProducts();
    }, []);

    const handleViewProduct = (product: Product) => {
        // Add to history only if it's not the most recent item
        if (userHistory.length === 0 || userHistory[userHistory.length - 1].id !== product.id) {
            setUserHistory(prevHistory => [...prevHistory, product].slice(-5)); // Keep history to last 5 items
        }
    };

    const handleAddToCart = (product: Product) => {
        setCart(prevCart => [...prevCart, product]);
        setToastMessage(`"${product.name}" was added to your cart.`);
        setShowToast(true);
    };

    const fetchRecommendations = useCallback(async () => {
        if (userHistory.length === 0 && cart.length === 0) return;

        setIsLoading(true);
        setError(null);

        try {
            const newRecommendations = await getRecommendations(userHistory, cart);
            setRecommendations(newRecommendations);
        } catch (err) {
            setError("Sorry, we couldn't fetch recommendations at this time.");
            console.error(err);
        } finally {
            setIsLoading(false);
        }
    }, [userHistory, cart]);


    useEffect(() => {
        const timer = setTimeout(() => {
            if (userHistory.length > 0 || cart.length > 0) {
                 fetchRecommendations();
            }
        }, 1000); // Debounce to avoid rapid API calls

        return () => clearTimeout(timer);
    }, [userHistory, cart, fetchRecommendations]);
    
    // Pagination logic
    const indexOfLastProduct = currentPage * productsPerPage;
    const indexOfFirstProduct = indexOfLastProduct - productsPerPage;
    const currentProducts = products.slice(indexOfFirstProduct, indexOfLastProduct);

    const paginate = (pageNumber: number) => {
        setCurrentPage(pageNumber);
        window.scrollTo(0, 0); // Scroll to top on page change
    }

    return (
        <div className="font-sans">
            <Header />
            <main className="max-w-7xl mx-auto py-10 px-4 sm:px-6 lg:px-8">
                <div className="grid grid-cols-1 lg:grid-cols-3 gap-12 items-start">
                    <div className="lg:col-span-2">
                         {isProductsLoading ? (
                            <div className="flex justify-center items-center h-96">
                                <div className="animate-spin rounded-full h-16 w-16 border-b-4 border-indigo-600"></div>
                            </div>
                        ) : (
                            <div>
                                <h2 className="text-3xl font-bold tracking-tight text-gray-900 mb-8">Our Products</h2>
                                <ProductGrid products={currentProducts} onView={handleViewProduct} onAddToCart={handleAddToCart} />
                                <Pagination 
                                    productsPerPage={productsPerPage} 
                                    totalProducts={products.length} 
                                    currentPage={currentPage}
                                    paginate={paginate} 
                                />
                            </div>
                        )}
                    </div>
                    <div className="space-y-8 lg:sticky top-10">
                        <ShoppingCart cartItems={cart} />
                        <Recommendations recommendations={recommendations} isLoading={isLoading} error={error} />
                    </div>
                </div>
            </main>
            <Toast message={toastMessage} show={showToast} onClose={() => setShowToast(false)} />
        </div>
    );
};

export default App;