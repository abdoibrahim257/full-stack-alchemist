"use client";
import React from 'react';
import Form from './components/Form';
import UploadForm from './components/UploadForm';

export default function Home() {
  return (
    <div>
        {/* <Form /> this was a test form*/}
        <div className='text-center mt-10 mb-5 text-4xl font-bold text-gray-800'>
          <h1> Speech-To-Text</h1>
        </div>
        <UploadForm />
    </div>
  );
}
