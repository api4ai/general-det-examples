﻿using System;
using System.Net.Http;
using System.Text.Json.Nodes;

using MimeTypes;
using RestSharp;


/*
 * Use "demo" mode just to try api4ai for free. Free demo is rate limited.
 * For more details visit:
 *   https://api4.ai
 *
 * Use 'rapidapi' if you want to try api4ai via RapidAPI marketplace.
 * For more details visit:
 *   https://rapidapi.com/api4ai-api4ai-default/api/general-detection/details
 */

const String MODE = "demo";


/*
 * Your RapidAPI key. Fill this variable with the proper value if you want
 * to try api4ai via RapidAPI marketplace.
 */
const String RAPIDAPI_KEY = "";

String url;
Dictionary<String, String> headers = new Dictionary<String, String>();

switch (MODE) {
    case "demo":
        url = "https://demo.api4ai.cloud/general-det/v1/results";
        headers.Add("A4A-CLIENT-APP-ID", "sample");
        break;
    case "rapidapi":
        url = "https://general-detection.p.rapidapi.com/v1/results";
        headers.Add("X-RapidAPI-Key", RAPIDAPI_KEY);
        break;
    default:
        Console.WriteLine($"[e] Unsupported mode: {MODE}");
        return 1;
}

// Prepare request.
String image = args.Length > 0 ? args[0] : "https://storage.googleapis.com/api4ai-static/samples/general-det-1.jpg";
var client = new RestClient(new RestClientOptions(url) { ThrowOnAnyError = true });
var request = new RestRequest();
if (image.Contains("://")) {
    request.AddParameter("url", image);
} else {
    request.AddFile("image", image, MimeTypeMap.GetMimeType(Path.GetExtension(image)));
}
var jsonResponse = (await client.ExecutePostAsync(request)).Content!;

// Print raw response.
Console.WriteLine($"[i] Raw response:\n{jsonResponse}\n");

// Parse response and objects with confidence > 0.5.
JsonNode docRoot = JsonNode.Parse(jsonResponse)!.Root;
JsonArray objects = docRoot["results"]![0]!["entities"]![0]!["objects"]!.AsArray();
var confident = from c in objects
                select c!["entities"]![0]!["classes"]!.AsObject().Single() into cls
                    where cls.Value!.GetValue<double>() > 0.5
                    select cls;
Console.WriteLine($"[i] {confident.Count()} objects found with confidence above 0.5:");
foreach (var c in confident) {
    Console.WriteLine($"{c.Key}: {c.Value}");
}

return 0;