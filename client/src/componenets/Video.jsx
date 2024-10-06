import React from 'react';
import axios from 'axios';
import { Box, Image, Button, VStack, Text, Heading, useToast } from '@chakra-ui/react';

function Video() {
    const toast = useToast();

    const handleStop = () => {
        axios.post('http://127.0.0.1:8000/stop_detection')
            .then(response => {
                console.log("Last Frame Saved:", response.data);
                window.open('http://localhost:5173/display_image', '_blank');
                toast({
                    title: "Detection Stopped.",
                    description: "The last frame has been saved successfully.",
                    status: "success",
                    duration: 5000,
                    isClosable: true,
                    position: "top"
                });
            })
            .catch(error => {
                console.error("Error stopping detection:", error);
                toast({
                    title: "Error.",
                    description: "Could not stop detection. Please try again.",
                    status: "error",
                    duration: 5000,
                    isClosable: true,
                    position: "top"
                });
            });
    };

    return (
        <VStack
            justifyContent="center"
            alignItems="center"
            height="100vh"
            spacing={8}
            bgGradient="linear(to-r, gray.700, gray.900)"
            padding={4}
        >
            <Heading color="gray.100">Live Object Detection</Heading>
            <Box
                boxShadow="xl"
                rounded="lg"
                overflow="hidden"
                width="512px"
                border="2px solid"
                borderColor="gray.600"
                bg="gray.800"
            >
                <Image
                    src="http://127.0.0.1:8000/video_feed"
                    alt="Live Video Feed"
                    width="100%"
                    height="auto"
                />
            </Box>
            <Button
                colorScheme="red"
                size="lg"
                onClick={handleStop}
                _hover={{ bg: 'red.600' }}
                _active={{ bg: 'red.700' }}
                color="white"
            >
                Stop Detection
            </Button>
        </VStack>
    );
}

export default Video;
