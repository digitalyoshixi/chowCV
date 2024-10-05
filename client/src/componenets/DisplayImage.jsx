import React from 'react';

function DisplayImage() {
  return (
    <div>
      <h1>Last Detection Image</h1>
      <img 
        src="http://127.0.0.1:8000/display_image" 
        alt="Last Frame" 
        style={{ maxWidth: '100%', height: 'auto' }} // Ensures responsive image
      />
    </div>
  );
}

export default DisplayImage;