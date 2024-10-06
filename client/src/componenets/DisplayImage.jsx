import React, { useEffect, useState } from 'react';

function DisplayImage() {
    const [itemname, setItemname] = useState('');
    const [price, setPrice] = useState('');
    const [expiry, setExpiry] = useState('');
    const [info, setInfo] = useState('');

    useEffect(() => {
        // Fetch itemname, price, expiry, and info from the backend
        fetch('http://localhost:8000/api/return_item_data')
            .then(response => response.json())
            .then(data => {
                console.log("Fetched data:", data); // Log the entire fetched data

                if (data) {
                    setItemname(data.itemname || 'Unknown Item');  // Set itemname or a fallback message
                    setPrice(data.price || 'No price available');  // Set price or a fallback message
                    setExpiry(data.expiry || 'No expiry available'); // Set expiry or a fallback message
                    setInfo(data.info || 'No additional information'); // Set info or a fallback message
                }
            })
            .catch(error => console.error('Error fetching item data:', error));
    }, []);

    return (
        <div>
            <h1>Last Detected Image</h1>
            <img 
                src="http://127.0.0.1:8000/display_image" 
                alt="Last Frame" 
                style={{ maxWidth: '100%', height: 'auto' }} 
            />
            <p>Item Name: {itemname}</p>  {/* Display itemname */}
            <p>Price: {price}</p>        
            <p>Expiry: {expiry}</p>      
            <p>Info: {info}</p>          
        </div>
    );
}

export default DisplayImage;