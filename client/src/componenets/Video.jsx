import React from 'react';
import axios from 'axios';
import './Video.css'; // Make sure to create a Video.css file

function Video() {
    const handleStop = () => {
        axios.post('http://127.0.0.1:8000/stop_detection')
            .then(response => {
                console.log("Last Frame Saved:", response.data);
                console.log("Item Name:", response.data.itemname);
                console.log("Expiry:", response.data.expiry);
                console.log("Price:", response.data.price);
                console.log("Info:", response.data.info);
                window.open('http://localhost:5173/display_image', '_blank');
            })
            .catch(error => {
                console.error("Error stopping detection:", error);
                alert("Error stopping detection. Please try again.");
            });
    };

    return (
        <div className="video-container">
            <img 
                src="http://127.0.0.1:8000/video_feed" 
                alt="Live Video Feed" 
                className="video-feed"
            />
            <button className="stop-button" onClick={handleStop}>
                Stop Detection
            </button>
        </div>
    );
}

export default Video;