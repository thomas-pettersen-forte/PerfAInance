import Link from "next/link";

export default function Advice() {
    return (
        <div className="flex flex-col items-center justify-center min-h-screen p-8 sm:p-20 font-[family-name:var(--font-geist-sans)]">
            <h1 className="text-4xl font-bold">Advice Page</h1>
            <p className="mt-4 text-lg text-center">
                Welcome to the advice page. Here you will find valuable information and tips.
            </p>
            <Link href="/">
                <button className="mt-8 rounded-full border border-solid border-transparent transition-colors flex items-center justify-center bg-foreground text-background gap-2 hover:bg-[#383838] dark:hover:bg-[#ccc] text-sm sm:text-base h-10 sm:h-12 px-4 sm:px-5">
                    Go back to Home
                </button>
            </Link>
        </div>
    );
}