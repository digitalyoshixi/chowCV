import react, { useState, useEffect } from 'react'
import axios from 'axios';

function Video() {
  const [isStopped, setIsStopped] = useState(false);

  // Function to handle stop button click
  const handleStop = () => {
    setIsStopped(true); // Update state to stop detection

    // POST request to stop 
    axios.post('http://127.0.0.1:8000/stop_detection')
      .then(response => {
        console.log("Detection Stopped:", response.data);
      })
      .catch(error => {
        console.error("Error stopping detection:", error);
      });
  };

  return (
    <>
    <div>
        <img 
        src = "http://127.0.0.1:8000/video_feed"
        alt = "video"
        />
        <button onClick={handleStop} disabled={isStopped}>
          stop
        </button>
    </div>
    </>
  )
}

export default Video;
