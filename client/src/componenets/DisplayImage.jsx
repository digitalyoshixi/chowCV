import React, { useEffect, useState } from 'react';
import { Box, Image, Text, VStack, Heading, Stack, Divider, HStack } from '@chakra-ui/react';

function DisplayImage() {
    const [itemname, setItemname] = useState('');
    const [price, setPrice] = useState('');
    const [expiry, setExpiry] = useState('');
    const [info, setInfo] = useState('');

    useEffect(() => {
        fetch('http://localhost:8000/api/return_item_data')
            .then(response => response.json())
            .then(data => {
                setItemname(data.itemname || 'Unknown Item');
                setPrice(data.price || 'No price available');
                setExpiry(data.expiry || 'No expiry available');
                setInfo(data.info || 'No additional information');
            })
            .catch(error => console.error('Error fetching item data:', error));
    }, []);

    return (
        <HStack
            justifyContent="center"
            alignItems="center"
            height="100vh"
            spacing={10}
            bgGradient="linear(to-r, gray.100, gray.300)"
            padding={8}
        >
            <Box
                boxShadow="2xl"
                rounded="lg"
                overflow="hidden"
                width="512px"
                maxWidth="100%"
                border="2px solid"
                borderColor="green.500"
                bg="white"
            >
                <Image
                    src="http://127.0.0.1:8000/display_image"
                    alt="Last Frame"
                    width="100%"
                    height="auto"
                    maxHeight="512px"
                    objectFit="cover" // Use cover to fill the box
                />
            </Box>
            <Stack
                spacing={4}
                width="512px"
                maxWidth="100%"
                bg="white"
                boxShadow="md"
                padding={6}
                rounded="md"
                border="1px solid"
                borderColor="gray.300"
                textAlign="left"
            >
                <Heading size="md" color="green.500">Item Details</Heading>
                <Divider />
                <Text fontSize="lg" fontWeight="bold" color="orange.600">
                    Item Name: {itemname}
                </Text>
                <Text fontSize="lg" fontWeight="bold" color="blue.600">
                    Price: ${price}
                </Text>
                <Text fontSize="lg" fontWeight="bold" color="orange.600">
                    Expiry: {expiry} days
                </Text>
                <Text fontSize="md" color="gray.600">
                    Info: {info}
                </Text>
            </Stack>
        </HStack>
    );
}

export default DisplayImage;