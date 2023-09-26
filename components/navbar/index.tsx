import React from "react";
import Link from "next/link"

const Navbar: React.FC = () => {
    return (
        <div className="bg-secondary text-headline py-3">
            <div className="container mx-auto px-4 flex justify-between">
                <Link href="/"><a className="text-md font-bold">HACAPI</a></Link>
            </div>
        </div>
    );
};

export default Navbar;
