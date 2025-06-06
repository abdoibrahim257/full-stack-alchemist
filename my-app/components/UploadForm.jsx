import React, {useState} from 'react'
import { ToastContainer, toast } from 'react-toastify';

const UploadForm = () => {
  const [audioFile, setAudioFile] = useState(null);
  const [loading, setLoading] = useState(false);
  const [transcript, setTranscript] = useState('');
  const [transID, setTransID] = useState('');
  const [language, setLanguage] = useState('');

  // Use environment variable for API URL
  const API_URL = "https://full-stack-alchemist-production.up.railway.app";

  function handelFileSelect(event) {
    const file = event.target.files[0];
    if (file && file.type.startsWith('audio/')) {
      setAudioFile(file);
      console.log("Selected file:", file);
    } else {
      toast.error('incorrect file format', {
        position: "top-right",
        autoClose: false,
        hideProgressBar: false,
        closeOnClick: true,
        pauseOnHover: true,
        draggable: false,
        progress: undefined,
        theme: "light",
      });
      setAudioFile(null);
    }
  }

  function exportToSRT() {
    if (!transID) {
      toast.error('No SRT file name available', {
        position: "top-right",
        autoClose: 5000,
        hideProgressBar: false,
        closeOnClick: true,
        pauseOnHover: true,
        draggable: false,
        progress: undefined,
        theme: "light",
      });
      return;
    }

    fetch(`${API_URL}/getSRT/${transID}`, {
      method: 'GET',
      headers: {
        'Accept': 'application/srt',
      },
    })
    .then(response => {
      if (!response.ok) {
        throw new Error('Network response was not ok');
      }
      return response.blob();
    })
    .then(blob => {
      const url = window.URL.createObjectURL(blob);
      const a = document.createElement('a');
      const srtFileName = `srtFolder/transcript_${transID}.srt`;
      a.href = url;
      a.download = srtFileName;
      document.body.appendChild(a);
      a.click();
      a.remove();
      window.URL.revokeObjectURL(url);
      toast.success('SRT file downloaded successfully', {
        position: "top-right",
        autoClose: 5000,
        hideProgressBar: false,
        closeOnClick: true,
        pauseOnHover: true,
        draggable: false,
        progress: undefined,
        theme: "light",
      });
    })
    .catch(error => {
      console.error('Error downloading SRT file:', error);
      toast.error('Error downloading SRT file', {
        position: "top-right",
        autoClose: 5000,
        hideProgressBar: false,
        closeOnClick: true,
        pauseOnHover: true,
        draggable: false,
        progress: undefined,
        theme: "light",
      });
    });
  }

  function handleAudioSubmit(){
    const formData = new FormData();
    formData.append('file', audioFile);
    setTranscript(''); // Clear previous transcript

    setLoading(true);

    fetch(`${API_URL}/uploadfile`, {
      headers: {
        'Accept': 'application/json',
      },
      method: 'POST',
      body: formData,
    }).then(response => {
      if (!response.ok) {
        throw new Error('Network response was not ok');
      }
      return response;
    }).then(
      response => response.json()
    ).then(data => {
      console.log('Response data:', data);
      if (data.transcription) {
        setTranscript(data.transcription);
        setTransID(data.transcript_id);
        setLanguage(data.language);

        toast.success( `Transcript is now availble for ${data.filename}`, {
          position: "top-right",
          autoClose: 5000,
          hideProgressBar: false,
          closeOnClick: true,
          pauseOnHover: true,
          draggable: false,
          progress: undefined,
          theme: "light",
        });
      }

      setLoading(false);

    }
    ).catch(error => {
      console.error('Error:', error);
      toast.error('Error submitting audio file', {
        position: "top-right",
        autoClose: 5000,
        hideProgressBar: false,
        closeOnClick: true,
        pauseOnHover: true,
        draggable: false,
        progress: undefined,
        theme: "light",
      });
      setLoading(false);
    }); 
  }

  return (
    <div className='w-full flex flex-col gap-4 justify-center items-center mt-[2rem]'>
      <ToastContainer />
      <div className='sections'>
        <h2 className='title'>Upload Audio</h2>
        <div className='upload-area'>
          {!audioFile && <img src='upload.svg' width={60} height={60}></img>}
          {audioFile && (
            <div className='text-center'>
              <p className='text-lg font-medium text-gray-700'>{audioFile.name}</p>
              <p className='text-sm text-gray-500'>Size: {(audioFile.size / 1024).toFixed(2)} KB</p>
            </div>
          )}
          <label htmlFor="audioInput" className='hardcodedMarginReset font-medium text-sky-600 hover:cursor-pointer'>upload file from device</label>
          <input id="audioInput" type="file" accept="audio/*" style={{display: "none"}} onChange={handelFileSelect}/>
          <p className='text-[0.7rem] text-gray-500 md:text-base'>Supported formats: mp3 mp4 wav m4a..etc</p>
        </div>
        <button
          className={audioFile && !loading ? "uploadBtn" : "uploadBtn-off"}
          onClick={handleAudioSubmit}
          disabled={loading || !audioFile}
        >
          {loading ? "Transcribing..." : "Transcribe this"}
        </button>
      </div>
      
      <div className='sections'>
        <div className="flex justify-between items-center">
          <h2 className='title'>Transcript</h2>
          {language && transcript && <p className='text-right text-gray-500 text-xs sm:text-sm md:text-base'>Detected Language: {language}</p>}
        </div>
        {loading && 
          <div className='flex flex-col items-center justify-center'>
            <div className="loader"></div>
            <p className='text-center text-gray-500'>Transcribing...</p>
          </div>
        }

        {!loading && !audioFile && !transcript && <p className='text-center text-gray-500'>Please upload an audio file to see the transcript.</p>}
        {!loading && audioFile && !transcript && <p className='text-center text-gray-500'>Your transcript will appear here after processing.</p>}
        {!loading && transcript && 
          <div>
            <p className='transcript'> {transcript} </p>
              
            <div className='flex gap-2'>
              <button
                className='uploadBtn'
                onClick={() => setTranscript('')}
              >
                Clear Transcript
              </button>
              <button
                className='uploadBtn'
                onClick={exportToSRT}
              >
                Export To SRT
              </button>
            </div>
          </div>
        }

      </div>

    </div>
  )
}

export default UploadForm