import Axios from 'axios';

export const axios = Axios.create({
  baseURL: process.env.WEB_RASA_URL || 'http://localhost:5005',
});
