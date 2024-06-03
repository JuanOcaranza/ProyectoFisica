'use server';

import { fetchVideoById, deleteVideoById, editVideoById } from '@/lib/data';
import { revalidatePath } from 'next/cache';
import { redirect } from 'next/navigation';

export async function createVideo(prveState: any, formData: FormData) {
    return { message: "Video created" };
}

export async function deleteVideo(id: string) {
    await deleteVideoById(id);
    revalidatePath('/');
}

export async function processVideo(id: string) {
    const video = await fetchVideoById(id);
    if (video) {
        video.processed = false;
        const response = await fetch('http://localhost:8000/api/tracked_video', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                video_name: video.name,
                video_extension: video.extension,
                distance_elbow_wrist: video.distance_elbow_wrist,
                mass_weight: video.mass_weight,
                mass_forearm: video.mass_forearm,
                radius_bicep: video.radius_bicep,
                height_shoulder: video.height_shoulder,
            })
        });
        if (response.ok) {
            video.processed = true;
            const data = await response.json();
            video.calories = data.calories;
            video.calories_abs = data.calories_abs;
            video.calories_from_energy = data.calories_from_energy;
            video.calories_from_energy_abs = data.calories_from_energy_abs;
            editVideoById(id, video);
            revalidatePath('/');
            redirect(`/${id}`);
        }
    }
}