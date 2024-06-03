import { Video } from '@/lib/definitions';
import { readDB, writeDB } from '@/db/db'

const PAGE_SIZE = 10;
export async function fetchFilteredVideos(
    query: string,
    currentPage: number
): Promise<Video[]> {
    const videos : Video[] = readDB().videos;
    return videos
        .filter((video) => video.name.toLowerCase().includes(query.toLowerCase()))
        .slice((currentPage - 1) * PAGE_SIZE, currentPage * PAGE_SIZE)
        .map((video) => ({ ...video, arm: video.arm === 'right' ? 'right' : 'left' }));
}

export async function fetchVideosPages(query: string): Promise<number> {
    const videos : Video[] = readDB().videos;
    return Math.ceil(videos.filter((video) => video.name.toLowerCase().includes(query.toLowerCase())).length / PAGE_SIZE);
}

export async function fetchVideoById(id: string) {
    const videos : Video[] = readDB().videos;
    return videos.find((video) => video.id === id);
}

export async function deleteVideoById(id: string) {
    const videos : Video[] = readDB().videos;
    const newVideos = videos.filter((video) => video.id !== id);
    writeDB({ videos: newVideos });
}

export async function editVideoById(id: string, video: Video) {
    const videos : Video[] = readDB().videos;
    const newVideos = videos.map((v) => (v.id === id ? video : v));
    writeDB({ videos: newVideos });
}