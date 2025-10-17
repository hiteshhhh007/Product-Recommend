import React from 'react';
import type { Product } from '../types';

interface ProductCardProps {
  product: Product;
  onView: (product: Product) => void;
  onAddToCart: (product: Product) => void;
}

const ProductCard: React.FC<ProductCardProps> = ({ product, onView, onAddToCart }) => {
  return (
    <div className="bg-white rounded-xl shadow-sm overflow-hidden transition-all duration-300 hover:shadow-lg border border-gray-200 flex flex-col">
      <div className="relative">
        <img className="w-full h-52 object-cover" src={product.imageUrl} alt={product.name} />
        <span className="absolute top-3 right-3 bg-indigo-100 text-indigo-800 text-xs font-semibold px-2.5 py-1 rounded-full">{product.category}</span>
      </div>
      <div className="p-5 flex flex-col flex-grow">
        <h3 className="text-xl font-bold text-gray-900">{product.name}</h3>
        <p className="text-gray-600 mt-2 flex-grow">{product.description}</p>
        <div className="mt-4">
          <p className="text-2xl font-extrabold text-gray-900">${product.price.toFixed(2)}</p>
        </div>
      </div>
       <div className="p-5 pt-0 mt-auto grid grid-cols-2 gap-3">
        <button
          onClick={() => onView(product)}
          className="w-full px-4 py-2 text-sm font-semibold text-indigo-600 bg-white rounded-lg border-2 border-indigo-200 hover:border-indigo-600 hover:bg-indigo-50 transition-colors"
          aria-label={`View details for ${product.name}`}
        >
          View Details
        </button>
        <button
          onClick={() => onAddToCart(product)}
          className="w-full px-4 py-2 text-sm font-semibold text-white bg-indigo-600 rounded-lg hover:bg-indigo-700 transition-colors focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500"
          aria-label={`Add ${product.name} to cart`}
        >
          Add to Cart
        </button>
      </div>
    </div>
  );
};

export default ProductCard;