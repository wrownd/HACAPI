import React from "react";
import apiRoutes from "../utils/apiRoutes";

import Layout from "../components/layout";
import Drawer from "../components/drawer";

import { CopyBlock, solarizedLight } from "react-code-blocks";
     
const Home: React.FC = () => {
    return (
        <Layout>
            <div className="lg:grid lg:grid-cols-5 h-full">
                <Drawer />
                <div className="lg:col-span-4 p-8">
                    <h3 className="text-4xl text-headline font-bold">Get Started</h3>

                    <h3 className="text-2xl font-bold mt-10 my-2 text-headline">Base API URL</h3>
                    <CopyBlock
                        language="javascript"
                        text="https://hacapi.vercel.app"
                        showLineNumbers={false}
                        theme={solarizedLight}
                        wrapLines={true}
                        codeBlock
                    />

                    <h3 className="text-2xl font-bold mt-10 my-2 text-headline">Example API Request</h3>
                    <CopyBlock
                        language="javascript"
                        text={`axios.get("hacapi.vercel.app${apiRoutes[0].exampleRequest}").then((res) => {
    console.log(res.data);
}).catch((error) => {
    console.log(error);
})`}
                        showLineNumbers={false}
                        theme={solarizedLight}
                        wrapLines={true}
                        codeBlock
                    />

                    <h3 className="text-2xl font-bold mt-10 my-2 text-headline">Example API Response</h3>
                    <CopyBlock
                        language="javascript"
                        text={apiRoutes[0].exampleResponse}
                        showLineNumbers={false}
                        theme={solarizedLight}
                        wrapLines={true}
                        codeBlock
                    />
    

                    <h3 className="text-2xl font-bold mt-10 my-2 text-headline">Security</h3>
                    <p>No user information is stored in any databases. All of the proccessing that happens in a request is dumped once the request has resolved.</p>
                </div>
            </div>
        </Layout>
    )
}

export default Home;