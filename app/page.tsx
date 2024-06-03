import Pagination from '@/components/pagination';
import Search from '@/components/search';
import { NewVideo } from '@/components/buttons';
import { VideosGridSkeleton } from '@/components/skeletons';
import { Suspense } from 'react';
import { fetchVideosPages } from '@/lib/data';
import VideosGrid from '@/components/videos-grid';

export default async function Page({
    searchParams,
}: {
    searchParams?: {
        query?: string;
        page?: string;
    };
}) {
    const query = searchParams?.query || '';
    const currentPage = Number(searchParams?.page) || 1;

    const totalPages = await fetchVideosPages(query);

    return (
        <div className="w-full">
            <div className="mt-1 flex items-center justify-between gap-2 md:mt-8">
                <Search placeholder="Search videos..." />
                <NewVideo />
            </div>
            <Suspense key={query + currentPage} fallback={<VideosGridSkeleton />}>
                <VideosGrid query={query} currentPage={currentPage} />
            </Suspense>
            <div className="mt-5 flex w-full justify-center">
                <Pagination totalPages={totalPages} />
            </div>
        </div>
    );
}