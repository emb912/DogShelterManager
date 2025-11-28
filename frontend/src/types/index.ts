export const DogSize = {
  small: "small",
  medium: "medium",
  large: "large",
} as const;

export type DogSize = typeof DogSize[keyof typeof DogSize];

export const DogStatus = {
  arrived: "arrived",
  adopted: "adopted",
  returned: "returned",
} as const;

export type DogStatus = typeof DogStatus[keyof typeof DogStatus];

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

export type DogCreate = Omit<Dog, 'id'>;
export type DogUpdate = Partial<DogCreate>;

export interface DogStats {
  current_in_shelter: number;
  adopted_total: number;
  returned_total: number;
  all_dogs_total: number;
}
