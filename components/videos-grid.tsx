import { Video } from "@/lib/definitions";
import VideoCard from "@/components/video-card";
import { fetchFilteredVideos } from "@/lib/data";

export default async function VideosGrid({
    query,
    currentPage,
}: {
    query: string;
    currentPage: number;
}) {
    const videos = await fetchFilteredVideos(query, currentPage);

    return (
        <div className="mt-6 flow-root">
            <div className="inline-block min-w-full align-middle">
                <div className="rounded-lg bg-slate-900 p-4">
                    <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-6">
                        {videos?.map((video) => (
                            <VideoCard key={video.id} video={video} />
                        ))}
                    </div>
                </div>
            </div>
        </div>
    );
}
