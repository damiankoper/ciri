import Axios from 'axios';

export const axios = Axios.create({
  baseURL: import.meta.env.VITE_WEB_RASA_URL || 'http://localhost:5005',
});
