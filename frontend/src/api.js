import axios from 'axios';

const API_URL = 'http://127.0.0.1:8000/api';

export const api = axios.create({
    baseURL: API_URL,
});

export const uploadBatch = async (files) => {
    const formData = new FormData();
    files.forEach(file => {
        formData.append('files', file);
    });
    const response = await api.post('/batches/upload/', formData);
    return response.data;
};

export const startExperiment = async (batchId, mode) => {
    const response = await api.post('/experiments/start/', {
        batch_id: batchId,
        mode: mode // 'SERIAL' or 'PARALLEL'
    });
    return response.data;
};

export const getExperimentStatus = async (experimentId) => {
    const response = await api.get(`/experiments/${experimentId}/`);
    return response.data;
};