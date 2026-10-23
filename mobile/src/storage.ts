import AsyncStorage from '@react-native-async-storage/async-storage';
import type { AskResult, DirectoryMember, Member } from './types';

const KEYS = {
  directory: 'agrisoko_directory', profile: 'agrisoko_last_profile', result: 'agrisoko_last_result',
};

async function read<T>(key: string): Promise<T | null> {
  const value = await AsyncStorage.getItem(key);
  if (!value) return null;
  try { return JSON.parse(value) as T; } catch { return null; }
}

export const storage = {
  getDirectory: () => read<DirectoryMember[]>(KEYS.directory),
  setDirectory: (value: DirectoryMember[]) => AsyncStorage.setItem(KEYS.directory, JSON.stringify(value)),
  getProfile: () => read<Member>(KEYS.profile),
  setProfile: (value: Member) => AsyncStorage.setItem(KEYS.profile, JSON.stringify(value)),
  getResult: () => read<AskResult>(KEYS.result),
  setResult: (value: AskResult) => AsyncStorage.setItem(KEYS.result, JSON.stringify(value)),
};

