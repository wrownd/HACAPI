import React from "react";
import Head from 'next/head'

import Navbar from "../navbar";

interface Props {
  children: React.ReactNode;
}

const Layout: React.FC<Props> = ({ children }) => {
  return (
    <>
    <Head>
      <title>HACAPI</title>
      <meta name="description" content="Access student data in HAC with HACAPI"></meta>
      <meta name="viewport" content="width=device-width, initial-scale=1" />
    </Head>
      <div className="bg-background flex flex-col h-full text-paragraph">
        <Navbar />

        {children}
      </div>
    </>
  );
};

export default Layout;
