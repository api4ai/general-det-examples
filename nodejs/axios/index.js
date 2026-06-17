#!/usr/bin/env node

// Example of using API4AI general objects detection.
const fs = require('fs')
const path = require('path')
const axios = require('axios').default
const FormData = require('form-data')

// Use 'normal' mode if you have an API Key from the API4AI Developer Portal. This is the method that users should normally prefer.
//
// Use 'rapidapi' if you want to try api4ai via RapidAPI marketplace.
// For more details visit:
//   https://rapidapi.com/api4ai-api4ai-default/api/general-detection/details
const MODE = 'normal'

// Your API4AI key. Fill this variable with the proper value if you have one.
const API4AI_KEY = ''

// Your RapidAPI key. Fill this variable with the proper value if you want
// to try api4ai via RapidAPI marketplace.
const RAPIDAPI_KEY = ''

const OPTIONS = {
  normal: {
    url: 'https://api4ai.cloud/general-det/v1/results',
    headers: { 'X-API-KEY': API4AI_KEY }
  },
  rapidapi: {
    url: 'https://general-detection.p.rapidapi.com/v1/results',
    headers: { 'X-RapidAPI-Key': RAPIDAPI_KEY }
  }
}

// Parse args: path or URL to image.
const image = process.argv[2] || 'https://static.api4.ai/samples/general-det-1.jpg'

// Preapare request: form.
const form = new FormData()
if (image.includes('://')) {
  // Data from image URL.
  form.append('url', image)
} else {
  // Data from local image file.
  const fileName = path.basename(image)
  form.append('image', fs.readFileSync(image), fileName)
}

// Preapare request: headers.
const headers = {
  ...OPTIONS[MODE].headers,
  ...form.getHeaders(),
  'Content-Length': form.getLengthSync()
}

// Make request.
axios.post(OPTIONS[MODE].url, form, { headers })
  .then(function (response) {
    // Print raw response.
    console.log(`💬 Raw response:\n${JSON.stringify(response.data)}\n`)
    // Parse response and objects with confidence > 0.5.
    const confident = response.data.results[0].entities[0].objects
      .map((obj) => obj.entities[0].classes)
      .filter((cls) => Object.values(cls)[0] > 0.5)
    console.log(`💬 ${confident.length} objects found with confidence above 0.5:\n${JSON.stringify(confident)}\n`)
  })
