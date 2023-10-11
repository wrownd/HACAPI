import type { NextPage } from 'next'

const Home: NextPage = () => {
  return (
      <div className="h-full flex flex-col justify-between">
        <div className='h-full flex flex-col justify-center items-center'>
          <h1 className='text-7xl font-bold text-headline text-center'>HACAPI</h1>
          <h2 className='text-paragraph text-center'>Built by William Rownd for the MyGrade application.</h2>
        </div>
      </div>
  )
}

export default Home
