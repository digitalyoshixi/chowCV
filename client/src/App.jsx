import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Video from './componenets/Video'; // Ensure the path is correct
import DisplayImage from './componenets/DisplayImage'; // Ensure the path is correct

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<Video />} />
        <Route path="/display_image" element={<DisplayImage />} /> {/* Ensure this matches the navigation path */}
      </Routes>
    </Router>
  );
}

export default App;