import React, { useEffect, useState } from 'react';
import './DisplayImage.css'; // Import the CSS file

function DisplayImage() {
    const [itemname, setItemname] = useState('');
    const [price, setPrice] = useState('');
    const [expiry, setExpiry] = useState('');
    const [info, setInfo] = useState('');

    useEffect(() => {
        fetch('http://localhost:8000/api/return_item_data')
            .then(response => response.json())
            .then(data => {
                setItemname(data.itemname || 'Unknown Item');
                setPrice(data.price || 'No price available');
                setExpiry(data.expiry || 'No expiry available');
                setInfo(data.info || 'No additional information');
            })
            .catch(error => console.error('Error fetching item data:', error));
    }, []);

    return (
        <div className="container">
            <h1>Last Detected Image</h1>
            <img src="http://127.0.0.1:8000/display_image" alt="Last Frame" />
            <div className="info">
                <p className="itemname">Item Name: {itemname}</p>
                <p className="price">Price: {price}</p>
                <p className="expiry">Expiry: {expiry}</p>
                <p className="infoText">Info: {info}</p>
            </div>
        </div>
    );
}

export default DisplayImage;