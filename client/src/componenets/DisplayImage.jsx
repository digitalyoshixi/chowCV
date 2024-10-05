import React from 'react';


function DisplayImage() {
  const [price, setText] = useState('');
  const [expiry, setExpiry] = useState('');

  useEffect(() => {
    fetch('http://localhost:5000/api/price')
      .then(response => response.json())
      .then(data => setText(data.price))
      .catch(error => console.error('Error:', error));
    fetch('http://localhost:5000/api/expiry')
      .then(response => response.json())
      .then(data => setText(data.expiry))
      .catch(error => console.error('Error:', error));
  }, []);


  return (
    <div>
      <h1>Last Detection Image</h1>
      <img 
        src="http://127.0.0.1:8000/display_image" 
        alt="Last Frame" 
        style={{ maxWidth: '100%', height: 'auto' }} // Ensures responsive image
      />
      <p>{price}</p>
      <p>{expiry}</p>
      
    </div>
  );
}

export default DisplayImage;