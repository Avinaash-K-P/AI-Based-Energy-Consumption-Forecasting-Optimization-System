import api from "./apiService";

export const getPipelineStatus = async () => {
  const response = await api.get("/ml/pipeline/status");
  return response.data;
};

export const getTrainingSummary = async () => {
  const response = await api.get("/ml/model/train-summary");
  return response.data;
};

export const getDashboardOverview = async () => {
  const [status, trainingSummary] = await Promise.all([
    getPipelineStatus(),
    getTrainingSummary(),
  ]);

  return {
    status,
    trainingSummary,
  };
};