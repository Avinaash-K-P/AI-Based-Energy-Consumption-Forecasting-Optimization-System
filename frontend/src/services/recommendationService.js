import api from "./apiService";

export const getOptimizationRecommendations = async ({
  forecastType,
  buildingId,
  deviceId,
}) => {
  const response = await api.get("/recommendations/optimization", {
    params: {
      forecast_type: forecastType,
      building_id: buildingId || undefined,
      device_id: deviceId || undefined,
    },
  });

  return response.data;
};