import { fetchVideoById } from "@/lib/data";
import { notFound } from "next/navigation";
import { Video } from "@/lib/definitions";
import { VideoPlayer } from "@/components/video-player";

export default async function Page({ params }: { params: { id: string } }) {
    const id = params.id;
    const video : Video | undefined = await fetchVideoById(id);

    if (!video) {
        notFound();
    }

    return (
        <div>
            <VideoPlayer path={"velocity_and_acceleration/" + video.name} />
            <VideoPlayer path={"forces/" + video.name} />
        </div>
    )
}