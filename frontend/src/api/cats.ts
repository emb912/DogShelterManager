import type { Cat, CatCreate, CatUpdate } from "../types";

const API_URL = "http://localhost:8000";

export const fetchCats = async (): Promise<Cat[]> => {
  const response = await fetch(`${API_URL}/cats`);
  if (!response.ok) {
    throw new Error("Failed to fetch cats");
  }
  return response.json();
};

export const createCat = async (cat: CatCreate): Promise<Cat> => {
  const response = await fetch(`${API_URL}/cats/`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(cat),
  });
  if (!response.ok) {
    throw new Error("Failed to create cat");
  }
  return response.json();
};

export const updateCat = async (id: number, cat: CatUpdate): Promise<Cat> => {
  const response = await fetch(`${API_URL}/cats/${id}`, {
    method: "PUT",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(cat),
  });
  if (!response.ok) {
    throw new Error("Failed to update cat");
  }
  return response.json();
};

export const deleteCat = async (id: number): Promise<void> => {
  const response = await fetch(`${API_URL}/cats/${id}`, {
    method: "DELETE",
  });
  if (!response.ok) {
    throw new Error("Failed to delete cat");
  }
};
