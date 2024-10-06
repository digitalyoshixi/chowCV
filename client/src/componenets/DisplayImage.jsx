import React, { useEffect, useState } from 'react';

function DisplayImage() {
  const [price, setPrice] = useState('');
  const [expiry, setExpiry] = useState('');

  useEffect(() => {
    // Fetch price and expiry
    fetch('http://localhost:8000/return_item_data')
      .then(response => response.json())
      .then(data => {
        setPrice(data.price);
        setExpiry(data.expiry); // Set expiry
      })
      .catch(error => console.error('Error fetching item data:', error));
  }, []);

  return (
    <div>
      <h1>Last Detection Image</h1>
      <img 
        src="http://127.0.0.1:8000/display_image" 
        alt="Last Frame" 
        style={{ maxWidth: '100%', height: 'auto' }} // Ensures responsive image
      />
      <p>Price: {price}</p>
      <p>Expiry: {expiry}</p> {/* Display the expiry */}
    </div>
  );
}

export default DisplayImage;