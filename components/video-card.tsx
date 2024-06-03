import { Video } from "@/lib/definitions";
import Image from "next/image";
import { EditVideo, DeleteVideo, SeeVideo, ProcessVideo } from "@/components/buttons";

export default function VideoCard({ video }: { video: Video }) {
    return (
        <div className="flex flex-col h-full relative bg-slate-800 rounded-md shadow-xl">
            <p className="p-2 text-xl text-center">{video.name}</p>
            <figure className="flex items-center justify-center grow"><Image src={"/posters/" + video.name + ".png"} alt={video.name + " poster"} width={200} height={200} /></figure>
            <div className="flex items-center justify-center m-2">
                <div className="flex justify-around items-center pt-2 gap-x-5">
                    <EditVideo id={video.id} />
                    <DeleteVideo id={video.id} />
                    <SeeVideo id={video.id} disabled={!video.processed} />
                    <ProcessVideo id={video.id} />
                </div>
            </div>
        </div>
    );
}