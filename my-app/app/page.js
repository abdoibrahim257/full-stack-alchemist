"use client";
import React from 'react';
import Form from '../components/Form';
import UploadForm from '../components/UploadForm';

export default function Home() {
  return (
    <div>
        {/* <Form /> this was a test form*/}
        <div className='text-center mt-10 mb-5'>
          <h1 className='header'> Speech-To-Text </h1>
          <p className='instruction'>Upload your audio file and get the transcript</p>
        </div>
        <UploadForm />
    </div>
  );
}
