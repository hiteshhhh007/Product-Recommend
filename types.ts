
export interface Product {
  id: number;
  name: string;
  category: string;
  price: number;
  imageUrl: string;
  description: string;
}

export interface Recommendation {
  product: Product;
  explanation: string;
}
