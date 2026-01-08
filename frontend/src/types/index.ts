export const DogSize = {
  small: "small",
  medium: "medium",
  large: "large",
} as const;

export type DogSize = (typeof DogSize)[keyof typeof DogSize];

export const DogStatus = {
  arrived: "arrived",
  adopted: "adopted",
  returned: "returned",
} as const;

export type DogStatus = (typeof DogStatus)[keyof typeof DogStatus];

export interface Dog {
  id: number;
  name: string;
  size: DogSize;
  birth_date: string | null;
  sex: string | null;
  neutered: boolean;
  admitted_date: string;
  released_date: string | null;
  status: DogStatus;
}

export type DogCreate = Omit<Dog, "id">;
export type DogUpdate = Partial<DogCreate>;

export interface DogStats {
  current_in_shelter: number;
  adopted_total: number;
  returned_total: number;
  all_dogs_total: number;
}

// Typy dla kotów
export const CatSize = {
  small: "small",
  medium: "medium",
  large: "large",
} as const;

export type CatSize = (typeof CatSize)[keyof typeof CatSize];

export const CatStatus = {
  arrived: "arrived",
  adopted: "adopted",
  returned: "returned",
} as const;

export type CatStatus = (typeof CatStatus)[keyof typeof CatStatus];

export interface Cat {
  id: number;
  name: string;
  size: CatSize;
  birth_date: string | null;
  sex: string | null;
  neutered: boolean;
  admitted_date: string;
  released_date: string | null;
  status: CatStatus;
  indoor_only: boolean;
}

export type CatCreate = Omit<Cat, "id">;
export type CatUpdate = Partial<CatCreate>;

export interface CatStats {
  current_in_shelter: number;
  adopted_total: number;
  returned_total: number;
  all_cats_total: number;
}

// Typ dla statusu serwera
export interface ServerStatus {
  status: string;
  started_at: string;
  last_activity: string | null;
}
