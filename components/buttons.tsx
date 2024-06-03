import { PencilIcon, PlusIcon, TrashIcon } from '@heroicons/react/24/outline';
import { LineChart, Cpu } from 'lucide-react';
import Link from 'next/link';
import { deleteVideo, processVideo } from '@/lib/actions';
import clsx from 'clsx';

const common_styles = 'rounded-md border p-2 transition-colors';

export function NewVideo() {
    return (
        <Link
            href="/create"
            className="flex h-10 items-center rounded-lg bg-blue-600 px-4 text-sm font-medium text-white transition-colors hover:bg-blue-500 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-blue-600"
        >
            <span className="hidden md:block">New Video</span>{' '}
            <PlusIcon className="h-5 md:ml-4" />
        </Link>
    );
}

export function EditVideo({ id }: { id: string }) {
    return (
        <Link
            href={`${id}/edit`}
            className={clsx(common_styles, ' bg-amber-500 hover:bg-amber-400 ')}
        >
            <PencilIcon className="w-5" />
        </Link>
    );
}

export function DeleteVideo({ id }: { id: string }) {
    return (
        <form action={deleteVideo.bind(null, id)}>
            <button type='submit' className={clsx(common_styles, 'bg-red-800 hover:bg-red-600')}>
                <span className="sr-only">Delete</span>
                <TrashIcon className="w-5" />
            </button>
        </form>
    );
}

export function SeeVideo({ id, disabled }: { id: string, disabled: boolean }) {
    return (
        <Link
            href={disabled ? '' : `${id}`}
            className={clsx(common_styles, disabled && "cursor-default hover:bg-inherit text-gray-600 border-gray-600", !disabled && "bg-emerald-800 hover:bg-emerald-600")}
            aria-disabled={disabled}
        >
            <LineChart className="w-5" />
        </Link>
    );
}

export function ProcessVideo({ id }: { id: string }) {
    return (
        <form action={processVideo.bind(null, id)}>
            <button type='submit' className={clsx(common_styles, 'bg-purple-900 hover:bg-purple-700')}>
                <span className="sr-only">Process</span>
                <Cpu className="w-5" />
            </button>
        </form>
    );
}