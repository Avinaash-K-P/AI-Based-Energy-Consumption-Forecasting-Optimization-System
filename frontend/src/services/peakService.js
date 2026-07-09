import api from "./apiService";

export const getFuturePeakPrediction = async ({
  forecastType,
  buildingId,
  deviceId,
}) => {
  const response = await api.get("/peak-prediction/future", {
    params: {
      forecast_type: forecastType,
      building_id: buildingId || undefined,
      device_id: deviceId || undefined,
    },
  });

  return response.data;
};

export const getHistoricalSpikes = async ({ buildingId, deviceId }) => {
  const response = await api.get("/peak-prediction/historical-spikes", {
    params: {
      building_id: buildingId || undefined,
      device_id: deviceId || undefined,
    },
  });

  return response.data;
};