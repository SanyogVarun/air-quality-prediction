const BASE_URL = "https://air-quality-prediction-yqua.onrender.com";

export async function fetchForecastData() {
  try {
    const response = await fetch(`${BASE_URL}/forecast`);
    if (!response.ok) throw new Error("Failed to fetch forecast data");
    const data = await response.json();
    return data;
  } catch (error) {
    console.error("API error:", error);
    return null;
  }
}
