import { API_BASE_URL, REQUEST_TIMEOUT_MS } from './config';
import type { AskResult, DirectoryMember, Member } from './types';

async function request<T>(path: string, options?: RequestInit): Promise<T> {
  const controller = new AbortController();
  const timeout = setTimeout(() => controller.abort(), REQUEST_TIMEOUT_MS);
  try {
    const response = await fetch(`${API_BASE_URL}${path}`, {
      ...options, signal: controller.signal,
      headers: {'Content-Type': 'application/json', ...(options?.headers ?? {})},
    });
    if (!response.ok) throw new Error(response.status === 404 ? 'Not found' : `Server error (${response.status})`);
    return await response.json() as T;
  } catch (error) {
    if (error instanceof Error && error.name === 'AbortError') throw new Error('Request timed out. Please try again.');
    throw error;
  } finally {
    clearTimeout(timeout);
  }
}

export const api = {
  members: () => request<DirectoryMember[]>('/members'),
  member: (id: string) => request<Member>(`/members/${encodeURIComponent(id)}`),
  ask: (question: string) => request<AskResult>('/ask', {method: 'POST', body: JSON.stringify({question})}),
  modelInfo: () => request<Record<string, unknown>>('/model-info'),
};

