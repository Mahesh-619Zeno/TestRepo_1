import config from './config';

function fetchData() {
  if (config.DEBUG_MODE) {
    console.log(`Debug: Fetching data from ${config.API_URL} with timeout ${config.TIMEOUT}ms`);
  }

  // Simulate API call
  return `Simulated request to ${config.API_URL} with timeout ${config.TIMEOUT}`;
}

const result = fetchData();
console.log(result);
