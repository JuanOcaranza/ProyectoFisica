export type Video = {
    id: string;
    name: string;
    extension: string;
    distance_elbow_wrist: number;
    mass_weight: number;
    mass_forearm: number;
    radius_bicep: number;
    height_shoulder: number;
    arm: 'left' | 'right';
    processed: boolean;
    calories: number;
    calories_abs: number;
    calories_from_energy: number;
    calories_from_energy_abs: number;
}