#!/usr/bin/env python3

"""Example of using API4AI general objects detection."""

import asyncio
import os
import sys

import aiohttp


# Use 'demo' mode just to try api4ai for free. Free demo is rate limited.
# For more details visit:
#   https://api4.ai
#
# Use 'rapidapi' if you want to try api4ai via RapidAPI marketplace.
# For more details visit:
#   https://rapidapi.com/api4ai-api4ai-default/api/general-detection/details
MODE = 'demo'


# Your RapidAPI key. Fill this variable with the proper value if you want
# to try api4ai via RapidAPI marketplace.
RAPIDAPI_KEY = ''


OPTIONS = {
    'demo': {
        'url': 'https://demo.api4ai.cloud/general-det/v1/results',
        'headers': {'A4A-CLIENT-APP-ID': 'sample'}
    },
    'rapidapi': {
        'url': 'https://general-detection.p.rapidapi.com/v1/results',
        'headers': {'X-RapidAPI-Key': RAPIDAPI_KEY}
    }
}


async def main():
    """Entry point."""
    image = sys.argv[1] if len(sys.argv) > 1 else 'https://storage.googleapis.com/api4ai-static/samples/general-det-1.jpg'

    # response = None
    async with aiohttp.ClientSession() as session:
        if '://' in image:
            # Data from image URL.
            data = {'url': image}
        else:
            # Data from local image file.
            data = aiohttp.MultipartWriter('form-data')
            payload = data.append(open(image, 'rb'))
            payload.set_content_disposition('form-data', name='image', filename=os.path.basename(image))
            payload.headers['Content-Type'] = payload.headers.pop('Content-Type')  # noqa: workaround for bad support of multipart/form-data in RapidAPI
        # Make request.
        async with session.post(OPTIONS[MODE]['url'],
                                data=data,
                                headers=OPTIONS[MODE]['headers']) as response:
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
