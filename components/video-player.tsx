export async function VideoPlayer({ path }: { path: string }) {

    return (
        <video controls aria-label="Video player">
            <source src={"/videos/" + path + ".mp4"} type="video/mp4" />
            Your browser does not support the video tag.
        </video>
    )
}