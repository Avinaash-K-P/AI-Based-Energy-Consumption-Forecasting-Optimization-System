import api from "./apiService";

export const getEnergyRecords = async (filters = {}) => {
  const response = await api.get("/energy-consumption/filter", {
    params: filters,
  });

  return response.data;
};

export const getEnergyForecast = async ({
  forecastType,
  buildingId,
  deviceId,
}) => {
  const response = await api.get("/energy-consumption/forecast", {
    params: {
      forecast_type: forecastType,
      building_id: buildingId || undefined,
      device_id: deviceId || undefined,
    },
  });

  return response.data;
};

export const getAllEnergyRecords = async () => {
  const response = await api.get("/energy-consumption/list");
  return response.data;
};