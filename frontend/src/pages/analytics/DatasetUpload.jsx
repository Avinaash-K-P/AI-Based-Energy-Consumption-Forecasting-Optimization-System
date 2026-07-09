import { useEffect, useState } from "react";
import {
  getPipelineStatus,
  getTrainingSummary,
  uploadDataset,
} from "../../services/mlPipelineService";
import "/src/styles/dataset.css"
import {toast} from "react-toastify";

const DatasetUpload = () => {
  const [selectedFile, setSelectedFile] = useState(null);
  const [status, setStatus] = useState(null);
  const [trainingSummary, setTrainingSummary] = useState(null);
  const [uploadResult, setUploadResult] = useState(null);
  const [loading, setLoading] = useState(false);

  const fetchStatus = async () => {
    try {
      const [statusData, trainingData] = await Promise.all([
        getPipelineStatus(),
        getTrainingSummary(),
      ]);

      setStatus(statusData);
      setTrainingSummary(trainingData);
    } catch (error) {
      console.error("Pipeline status error:", error);
    }
  };

  useEffect(() => {
    fetchStatus();
  }, []);

  const handleUpload = async (event) => {
    event.preventDefault();

    if (!selectedFile) {
      setUploadResult({
        message: "Please select a CSV file before uploading.",
      });
      return;
    }

    try {
      setLoading(true);

      const result = await uploadDataset(selectedFile);
      setUploadResult(result);
      await fetchStatus();
      toast.success("Dataset uploaded successfully!")
    } catch (error) {
      setUploadResult({
        message:
          error.response?.data?.detail ||
          "Dataset upload failed. Please check the file format.",
      });
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="dashboard-page">
      <div className="page-header">
        <h1>Dataset Upload</h1>
        <p>Upload CSV energy consumption data for forecasting and analytics</p>
      </div>

      <div className="dashboard-section">
        <form className="upload-panel" onSubmit={handleUpload}>
          <label>CSV Dataset</label>

          <input
            type="file"
            accept=".csv"
            onChange={(event) => setSelectedFile(event.target.files[0])}
          />

          <button type="submit" disabled={loading}>
            {loading ? "Uploading..." : "Upload Dataset"}
          </button>
        </form>

        {uploadResult && (
          <div className="summary-panel">
            <p>{uploadResult.message}</p>

            {"total_rows" in uploadResult && (
              <>
                <p>
                  <strong>Total Rows:</strong> {uploadResult.total_rows}
                </p>
                <p>
                  <strong>Inserted Rows:</strong> {uploadResult.inserted_rows}
                </p>
                <p>
                  <strong>Skipped Rows:</strong> {uploadResult.skipped_rows}
                </p>
              </>
            )}
          </div>
        )}
      </div>

      <div className="kpi-grid">
        <div className="kpi-card">
          <span>Total Records</span>
          <strong>{status?.total_energy_records || 0}</strong>
        </div>

        <div className="kpi-card">
          <span>Buildings</span>
          <strong>{status?.total_buildings || 0}</strong>
        </div>

        <div className="kpi-card">
          <span>Devices</span>
          <strong>{status?.total_devices || 0}</strong>
        </div>

        <div className="kpi-card">
          <span>Model Status</span>
          <strong>{trainingSummary?.model_status || "unknown"}</strong>
        </div>
      </div>
    </div>
  );
};

export default DatasetUpload;