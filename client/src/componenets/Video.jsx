import React from 'react';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';

function Video() {
    const navigate = useNavigate();

    const handleStop = () => {
        // POST request to stop detection and save the last frame
        axios.post('http://127.0.0.1:8000/stop_detection')
            .then(response => {
                console.log("Last Frame Saved:", response.data);
                // Open the display image page in a new tab
                window.open('http://localhost:5173/display_image', '_blank');
            })
            .catch(error => {
                console.error("Error stopping detection:", error);
            });
    };

    return (
        <div>
            <img 
                src="http://127.0.0.1:8000/video_feed"
                alt="Live Video Feed"
            />
            <button onClick={handleStop}>
                stop
            </button>
        </div>
    );
}

export default Video;