import Image from "next/image";
import Link from "next/link";

export default function Home() {
    return (
        <div className="flex flex-col items-center justify-center min-h-screen p-8 sm:p-20 font-[family-name:var(--font-geist-sans)]">
            <h1 className="text-4xl font-bold">Velkommen til PerfAInance</h1>

            <Link href="/advice">
                <button className="rounded-full mt-8 border border-solid border-transparent transition-colors flex items-center justify-center bg-foreground text-background gap-2 hover:bg-[#383838] dark:hover:bg-[#ccc] text-sm sm:text-base h-10 sm:h-12 px-4 sm:px-5">
                    Kom i gang
                </button>
            </Link>
        </div>
    );
}