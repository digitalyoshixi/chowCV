import react, { useState, useEffect } from 'react'

function Video() {
  const [count, setCount] = useState(0)

  return (
    <>
    <div>
        <img 
        src = "http://127.0.0.1:8000/video_feed"
        alt = "video"
        />
        
    </div>
    </>
  )
}

export default Video;
