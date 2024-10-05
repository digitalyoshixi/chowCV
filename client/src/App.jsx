import react, { useState, useEffect } from 'react'
import Video from './componenets/Video'

function App() {
  const [count, setCount] = useState(0)

  return (
    <>
      <div>
        <Video/>
      </div>
      <p className="read-the-docs">
        Click on the Vite and React logos to learn more
      </p>
    </>
  )
}

export default App;
