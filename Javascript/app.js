// app.js

const config = require('./config');

// Simulate a fetch function
function fetchData(endpoint) {
  const url = `${config.API_URL}${endpoint}`;

  if (config.DEBUG_MODE) {
    console.log(`[DEBUG] Preparing to fetch: ${url}`);
    console.log(`[DEBUG] Timeout set to: ${config.TIMEOUT}ms`);
  }

  return new Promise((resolve, reject) => {
    setTimeout(() => {
      // Simulate success/failure
      const success = Math.random() > 0.2; // 80% success rate

      if (success) {
        const data = { message: "Data fetched successfully", url };
        if (config.DEBUG_MODE) {
          console.log(`[DEBUG] Fetch success:`, data);
        }
        resolve(data);
      } else {
        const error = new Error("Failed to fetch data");
        if (config.DEBUG_MODE) {
          console.error(`[DEBUG] Fetch error:`, error.message);
        }
        reject(error);
      }
    }, config.TIMEOUT);
  });
}

// Main function to execute logic
async function main() {
  try {
    const data = await fetchData("/users");
    console.log("✅ Response:", data);
  } catch (err) {
    console.error("❌ Error:", err.message);
  }
}

main();
