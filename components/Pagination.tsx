import React from 'react';

interface PaginationProps {
  productsPerPage: number;
  totalProducts: number;
  currentPage: number;
  paginate: (pageNumber: number) => void;
}

const Pagination: React.FC<PaginationProps> = ({ productsPerPage, totalProducts, currentPage, paginate }) => {
  const pageNumbers = [];
  const totalPages = Math.ceil(totalProducts / productsPerPage);

  for (let i = 1; i <= totalPages; i++) {
    pageNumbers.push(i);
  }
  
  const handlePrev = () => {
    if (currentPage > 1) {
        paginate(currentPage - 1);
    }
  }
  
  const handleNext = () => {
    if (currentPage < totalPages) {
        paginate(currentPage + 1);
    }
  }

  if (totalPages <= 1) return null;

  return (
    <nav className="mt-12 flex items-center justify-between" aria-label="Pagination">
      <div className="flex-1 flex justify-start">
         <button
          onClick={handlePrev}
          disabled={currentPage === 1}
          className="relative inline-flex items-center px-4 py-2 border border-gray-300 text-sm font-medium rounded-md text-gray-700 bg-white hover:bg-gray-50 disabled:opacity-50 disabled:cursor-not-allowed"
        >
          Previous
        </button>
      </div>
      <div className="hidden md:flex">
        {pageNumbers.map(number => (
          <button
            key={number}
            onClick={() => paginate(number)}
            className={`relative inline-flex items-center px-4 py-2 border text-sm font-medium ${
              currentPage === number
                ? 'z-10 bg-indigo-50 border-indigo-500 text-indigo-600'
                : 'bg-white border-gray-300 text-gray-500 hover:bg-gray-50'
            } ${number === 1 ? 'rounded-l-md' : ''} ${number === totalPages ? 'rounded-r-md' : '-ml-px'}`}
          >
            {number}
          </button>
        ))}
      </div>
       <div className="flex-1 flex justify-end">
        <button
          onClick={handleNext}
          disabled={currentPage === totalPages}
          className="relative inline-flex items-center px-4 py-2 border border-gray-300 text-sm font-medium rounded-md text-gray-700 bg-white hover:bg-gray-50 disabled:opacity-50 disabled:cursor-not-allowed"
        >
          Next
        </button>
      </div>
    </nav>
  );
};

export default Pagination;