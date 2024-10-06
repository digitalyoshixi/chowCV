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
              
              // Optionally, you can show a confirmation alert
              alert("Detection stopped and last frame saved! Check the new tab for details.");
          })
          .catch(error => {
              console.error("Error stopping detection:", error);
              alert("Error stopping detection. Please try again."); // Show error alert
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