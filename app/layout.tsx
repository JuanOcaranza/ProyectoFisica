import './globals.css';
import { inter } from '@/components/fonts';
import { Metadata } from 'next';

export const metadata: Metadata = {
    title: {
        template: '%s | Proyecto Física',
        default: 'Proyecto Física',
    },
    description: 'Análisis del consumo de calorias en curl de bicep',
};
export default function RootLayout({
    children,
}: {
    children: React.ReactNode;
}) {
    return (
        <html lang="en">
            <body className={`${inter.className} antialiased bg-gray-800 text-slate-100`}>
                <div className="p-2 md:px-12 lg:px-32">{children}</div>
            </body>
        </html>
    );
}
