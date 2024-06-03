export default function TextFormField({ name, label, required }: { name: string, label: string, required: boolean }) {
    return (
        <div>
            <label htmlFor={name} className="block text-sm font-medium text-gray-300">
                {label}
            </label>
            <div className="mt-1">
                <input
                    type="text"
                    name={name}
                    id={name}
                    className="block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm"
                    required={required}
                />
            </div>
        </div>
    );

}