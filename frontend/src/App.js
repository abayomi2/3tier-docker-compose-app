// frontend/src/App.js
import React, { useEffect, useState } from 'react';

function App() {
  const [products, setProducts] = useState([]);

  useEffect(() => {
  const apiUrl = process.env.REACT_APP_API_URL || 'http://localhost:5000'; // Fallback if env variable isn't set
  fetch(`${apiUrl}/products`) // Use backticks for template literals
    .then((response) => response.json())
    .then((data) => setProducts(data))
    .catch((error) => console.error('Error fetching products:', error));
}, []);


  return (
    <div>
      <h1>Product List</h1>
      <ul>
        {products.map((product) => (
          <li key={product.id}>{product.name}</li>
        ))}
      </ul>
    </div>
  );
}

export default App;
