// Example Netlify Function that mimics a simple save/read endpoint
// Drop this file into `netlify/functions/` and Netlify will expose it at
// /.netlify/functions/save when deployed or when running `netlify dev`.

exports.handler = async function (event, context) {
  // You can inspect event.httpMethod, event.body, event.queryStringParameters, etc.
  if (event.httpMethod === 'POST') {
    // In a real function you would validate input and save to a DB or storage.
    const payload = event.body ? JSON.parse(event.body) : {};
    return {
      statusCode: 200,
      body: JSON.stringify({ ok: true, message: 'Received POST', data: payload }),
    };
  }

  // Default: return a small README for the endpoint
  return {
    statusCode: 200,
    body: JSON.stringify({
      ok: true,
      message: 'Netlify function is working. Use POST to send data.',
      methods: ['GET', 'POST'],
    }),
  };
};
