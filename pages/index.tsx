import type { NextPage } from 'next'
import Link from "next/link"

import Layout from '../components/layout'

const Home: NextPage = () => {
  return (
    <Layout>
      <div className="h-full flex flex-col justify-between">
        <div className='h-full flex flex-col justify-center items-center'>
          <h1 className='text-7xl font-bold text-headline text-center'>HACAPI</h1>
          <h2 className='text-paragraph text-center'>This page will be private soon.</h2>

          <Link href="/home"><button className='bg-highlight text-main py-2 px-14 mt-8 rounded-md active:bg-sky-600'>Docs</button></Link>
        </div>
      </div>
    </Layout>
  )
}

export default Home
