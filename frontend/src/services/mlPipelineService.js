import api from "./apiService";

export const uploadDataset = async (file) => {
  const formData = new FormData();
  formData.append("file", file);

  const response = await api.post("/ml/dataset/upload", formData, {
    headers: {
      "Content-Type": "multipart/form-data",
    },
  });

  return response.data;
};

export const getPipelineStatus = async () => {
  const response = await api.get("/ml/pipeline/status");
  return response.data;
};

export const getTrainingSummary = async () => {
  const response = await api.get("/ml/model/train-summary");
  return response.data;
};