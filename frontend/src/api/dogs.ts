import type { Dog, DogCreate, DogUpdate } from '../types';

const API_URL = 'http://localhost:8000';

export const fetchDogs = async (): Promise<Dog[]> => {
  const response = await fetch(`${API_URL}/dogs`);
  if (!response.ok) {
    throw new Error('Failed to fetch dogs');
  }
  return response.json();
};

export const createDog = async (dog: DogCreate): Promise<Dog> => {
  const response = await fetch(`${API_URL}/dogs/`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(dog),
  });
  if (!response.ok) {
    throw new Error('Failed to create dog');
  }
  return response.json();
};

export const updateDog = async (id: number, dog: DogUpdate): Promise<Dog> => {
  const response = await fetch(`${API_URL}/dogs/${id}`, {
    method: 'PUT',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(dog),
  });
  if (!response.ok) {
    throw new Error('Failed to update dog');
  }
  return response.json();
};

export const deleteDog = async (id: number): Promise<void> => {
  const response = await fetch(`${API_URL}/dogs/${id}`, {
    method: 'DELETE',
  });
  if (!response.ok) {
    throw new Error('Failed to delete dog');
  }
};

