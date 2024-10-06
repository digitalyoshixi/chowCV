import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { ChakraProvider, extendTheme } from '@chakra-ui/react';
import Video from './componenets/Video';
import DisplayImage from './componenets/DisplayImage';

const theme = extendTheme({
  fonts: {
    heading: "'Roboto', sans-serif",
    body: "'Open Sans', sans-serif",
  },
  colors: {
    brand: {
      500: "#1a202c",
      600: "#2d3748",
    },
  },
});

function App() {
  return (
    <ChakraProvider theme={theme}>
      <Router>
        <Routes>
          <Route path="/" element={<Video />} />
          <Route path="/display_image" element={<DisplayImage />} />
        </Routes>
      </Router>
    </ChakraProvider>
  );
}

export default App;