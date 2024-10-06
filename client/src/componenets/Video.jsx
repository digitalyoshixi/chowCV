import React from 'react';
import axios from 'axios';

function Video() {

    const handleStop = () => {
        // POST request to stop detection and save the last frame
        axios.post('http://127.0.0.1:8000/stop_detection')
            .then(response => {
                console.log("Last Frame Saved:", response.data);
                
                // Log the database result to the browser's console
                console.log("Database Result:");
                console.log("Item Name:", response.data.itemname);
                console.log("Expiry:", response.data.expiry);
                console.log("Price:", response.data.price);
                console.log("Info:", response.data.info);

                // Open the display image page in a new tab
                window.open('http://localhost:5173/display_image', '_blank');  // Open in a new tab
            })
            .catch(error => {
                console.error("Error stopping detection:", error);
                alert("Error stopping detection. Please try again."); // You can keep this alert for errors
            });
    };

    return (
        <div>
            <img 
                src="http://127.0.0.1:8000/video_feed" 
                alt="Live Video Feed"
            />
            <button onClick={handleStop}>
                Stop
            </button>
        </div>
    );
}

export default Video;