export const API_BASE_URL = (process.env.EXPO_PUBLIC_API_BASE_URL ?? 'http://10.0.2.2:8000').replace(/\/$/, '');
export const GROUP_CODE = process.env.EXPO_PUBLIC_GROUP_CODE ?? 'COMBO_A3_G05';
export const APP_VERSION = '1.0.0';
export const MAX_QUESTION_LENGTH = 300;
export const REQUEST_TIMEOUT_MS = 5_000;

