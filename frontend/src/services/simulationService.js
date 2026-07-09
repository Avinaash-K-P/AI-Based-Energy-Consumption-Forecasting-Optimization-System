import api from "./apiService";

export const runSimulation = async (payload) => {
  const response = await api.post("/simulation/run", payload);
  return response.data;
};