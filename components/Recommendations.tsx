import React from 'react';
import type { Recommendation } from '../types';
import LoadingSpinner from './LoadingSpinner';

interface RecommendationsProps {
  recommendations: Recommendation[];
  isLoading: boolean;
  error: string | null;
}

const Recommendations: React.FC<RecommendationsProps> = ({ recommendations, isLoading, error }) => {
  return (
    <div className="bg-white p-6 rounded-xl shadow-sm border border-gray-200">
      <h3 className="text-xl font-bold text-gray-900 mb-1 flex items-center">
        <svg xmlns="http://www.w3.org/2000/svg" className="h-6 w-6 mr-3 text-indigo-600" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth="2">
             <path strokeLinecap="round" strokeLinejoin="round" d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z" />
        </svg>
        Just For You
      </h3>
      <p className="text-sm text-gray-500 mb-4 ml-9">AI-Powered Suggestions</p>
      
      {isLoading && <LoadingSpinner />}
      {error && <p className="text-red-500 px-2 text-sm">{error}</p>}
      
      {!isLoading && !error && recommendations.length === 0 && (
        <div className="text-center py-6 px-4 bg-gray-50 rounded-lg">
            <p className="text-gray-600 text-sm">View products or add items to your cart to get personalized recommendations!</p>
        </div>
      )}

      <div className="space-y-4">
        {recommendations.map(({ product, explanation }) => (
          <div key={product.id} className="flex items-start space-x-4">
            <img src={product.imageUrl} alt={product.name} className="w-24 h-24 rounded-lg object-cover flex-shrink-0 border border-gray-200" />
            <div className="flex-grow">
              <h4 className="font-bold text-gray-900">{product.name}</h4>
              <p className="text-sm text-gray-600 mt-2 p-3 bg-gray-50 border-l-4 border-indigo-300 rounded-r-lg">
                {explanation}
              </p>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};

export default Recommendations;