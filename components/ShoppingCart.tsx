import React from 'react';
import type { Product } from '../types';

interface ShoppingCartProps {
  cartItems: Product[];
}

const ShoppingCart: React.FC<ShoppingCartProps> = ({ cartItems }) => {
  const total = cartItems.reduce((sum, item) => sum + item.price, 0);

  return (
    <div className="bg-white p-6 rounded-xl shadow-sm border border-gray-200">
      <h3 className="text-xl font-bold text-gray-900 mb-4 flex items-center">
        <svg xmlns="http://www.w3.org/2000/svg" className="h-6 w-6 mr-3 text-indigo-600" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth="2">
            <path strokeLinecap="round" strokeLinejoin="round" d="M3 3h2l.4 2M7 13h10l4-8H5.4M7 13L5.4 5M7 13l-2.293 2.293c-.63.63-.184 1.707.707 1.707H17m0 0a2 2 0 100 4 2 2 0 000-4zm-8 2a2 2 0 11-4 0 2 2 0 014 0z" />
        </svg>
        Shopping Cart
      </h3>
      {cartItems.length === 0 ? (
        <div className="text-center py-8">
            <p className="text-gray-500">Your cart is empty.</p>
        </div>
      ) : (
        <div className="space-y-3">
          {cartItems.map((item, index) => (
            <div key={`${item.id}-${index}`} className="flex justify-between items-center text-sm">
              <span className="text-gray-700 truncate pr-2">{item.name}</span>
              <span className="font-medium text-gray-900 flex-shrink-0">${item.price.toFixed(2)}</span>
            </div>
          ))}
          <div className="border-t border-gray-200 pt-4 mt-4">
            <div className="flex justify-between items-center font-bold text-base">
              <span>Total</span>
              <span>${total.toFixed(2)}</span>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default ShoppingCart;