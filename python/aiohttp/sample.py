#!/usr/bin/env python3

"""Example of using API4AI general objects detection."""

import asyncio
import sys

import aiohttp


# Use 'normal' mode if you have an API Key from the API4AI Developer Portal. This is the method that users should normally prefer.
#
# Use 'rapidapi' if you want to try api4ai via RapidAPI marketplace.
# For more details visit:
#   https://rapidapi.com/api4ai-api4ai-default/api/general-detection/details
MODE = 'normal'

# Your API4AI key. Fill this variable with the proper value if you have one.
API4AI_KEY = ''

# Your RapidAPI key. Fill this variable with the proper value if you want
# to try api4ai via RapidAPI marketplace.
RAPIDAPI_KEY = ''


OPTIONS = {
    'normal': {
        'url': 'https://api4ai.cloud/general-det/v1/results',
        'headers': {'X-API-KEY': API4AI_KEY}
    },
    'rapidapi': {
        'url': 'https://general-detection.p.rapidapi.com/v1/results',
        'headers': {'X-RapidAPI-Key': RAPIDAPI_KEY}
    }
}


async def main():
    """Entry point."""
    image = sys.argv[1] if len(sys.argv) > 1 else 'https://static.api4.ai/samples/general-det-1.jpg'

    async with aiohttp.ClientSession() as session:
        if '://' in image:
            # Data from image URL.
            data = {'url': image}
        else:
            # Data from local image file.
            data = {'image': open(image, 'rb')}
        # Make request.
        async with session.post(OPTIONS[MODE]['url'],
                                data=data,
                                headers=OPTIONS[MODE].get('headers')) as response:
            resp_json = await response.json()
            resp_text = await response.text()

        # Print raw response.
        print(f'💬 Raw response:\n{resp_text}\n')

        # Parse response and objects with confidence > 0.5.
        confident = [x['entities'][0]['classes']
                     for x in resp_json['results'][0]['entities'][0]['objects']
                     if list(x['entities'][0]['classes'].values())[0] > 0.5]

        print(f'💬 {len(confident)} objects found with confidence above 0.5:\n{confident}\n')


if __name__ == '__main__':
    # Run async function in asyncio loop.
    asyncio.run(main())
