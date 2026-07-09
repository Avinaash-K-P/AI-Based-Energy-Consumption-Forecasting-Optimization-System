import api from "./apiService";

export const detectAnomalies = async ({ buildingId, deviceId }) => {
  const response = await api.get("/anomalies/detect", {
    params: {
      building_id: buildingId || undefined,
      device_id: deviceId || undefined,
    },
  });

  return response.data;
};