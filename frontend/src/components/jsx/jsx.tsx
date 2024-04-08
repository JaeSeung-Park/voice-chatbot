// import React, { useState, useEffect } from 'react';
// import SpeechRecognition, { useSpeechRecognition } from 'react-speech-recognition';
// import axios from 'axios';

// interface Props {
//   isLoading: boolean;
//   setIsLoading: React.Dispatch<React.SetStateAction<boolean>>;
//   setList: React.Dispatch<React.SetStateAction<{ prompt: string | null; bot: any; }[]>>;
//   list: { prompt: string | null; bot: any; }[];
// }

// const Chatbot: React.FC<Props> = ({ isLoading, setIsLoading, setList, list }) => {
//     const [audioBlob, setAudioBlob] = useState<Blob | null>(null);
//     const [isRecording, setIsRecording] = useState<boolean>(false);
//     const { transcript, resetTranscript } = useSpeechRecognition();
//     let mediaRecorder: MediaRecorder | null = null;
//     let audioChunks: Blob[] = [];
  
//     const startRecording = () => {
//       if (!navigator.mediaDevices || !navigator.mediaDevices.getUserMedia) {
//         console.error('getUserMedia is not supported');
//         return;
//       }
  
//       navigator.mediaDevices.getUserMedia({ audio: true })
//         .then((stream) => {
//           mediaRecorder = new MediaRecorder(stream, { mimeType: 'audio/mpeg' });
//           mediaRecorder.ondataavailable = (event) => {
//             audioChunks.push(event.data);
//           };
//           mediaRecorder.start();
//           setIsRecording(true);
//           SpeechRecognition.startListening({ language: 'ko-KR', continuous: true });
//         })
//         .catch((error) => {
//           console.error('Error accessing microphone:', error);
//         });
//     };
  
//     const stopRecording = () => {
//       if (mediaRecorder && mediaRecorder.state !== 'inactive') {
//         mediaRecorder.stop();
//         mediaRecorder.onstop = () => {
//           const audioBlob = new Blob(audioChunks, { type: 'audio/mpeg' });
//           setAudioBlob(audioBlob);
//           audioChunks = [];
//           setIsRecording(false);
//           // After stopping recording, call the sendMessage function
//           sendMessage();
//         };
//       }
//       SpeechRecognition.stopListening();
//       setIsLoading(false);
//     };
  
//     const sendMessage = async () => {
//       try {
//         setList(prevList => [...prevList, { prompt: transcript, bot: null }]);
        
//         const formData = new FormData();
//         formData.append('text', transcript);
//         if (audioBlob) {
//           formData.append('audio', audioBlob);
//         }
//         const response = await axios.post('http://127.0.0.1:8000/api/chatbot/', formData);
//         console.log('Response from backend:', response.data);
  
//         // Play the response audio from the backend
//         const audioResponse = new Audio(response.data.output_audio_path);
//         audioResponse.play();
//       } catch (error) {
//         console.error('Error sending data:', error);
//       }
//     };
  
//     useEffect(() => {
//       // If there is a transcript and it is not empty, call sendMessage function
//       if (transcript && transcript.trim() !== '') {
//         sendMessage();
//         // After sending the message, reset the transcript
//         resetTranscript();
//       }
//     }, [transcript, resetTranscript]);
  
//     return (
//       <div>
//         {/* Show both start and stop buttons */}
//         <button onClick={startRecording}>시작</button>
//         <button onClick={stopRecording}>종료</button>
//         {/* Display transcript below the buttons */}
//         <p>입력: {transcript}</p>
//       </div>
//     );
//   };
  
// export default Chatbot;
//-----------------------------------------------------------------------------------------------------


// import React, { useState, useEffect } from 'react';
// import SpeechRecognition, { useSpeechRecognition } from 'react-speech-recognition';
// import axios from 'axios';
// // import Tts from 'react-native-tts';

// interface Props {
//   isLoading: boolean;
//   setIsLoading: React.Dispatch<React.SetStateAction<boolean>>;
//   setList: React.Dispatch<React.SetStateAction<{ prompt: string | null; bot: any; }[]>>;
//   list: { prompt: string | null; bot: any; }[];
// }

// const Chatbot: React.FC<Props> = ({ isLoading, setIsLoading, setList, list }) => {
//   const { transcript, resetTranscript } = useSpeechRecognition();
//   const [isRecording, setIsRecording] = useState<boolean>(false);
//   const [audioUrl, setAudioUrl] = useState<string>('');

//   const startRecording = () => {
//     setIsRecording(true);
//     SpeechRecognition.startListening({ language: 'ko-KR', continuous: true });
//   };

//   const stopRecording = () => {
//     setIsRecording(false);
//     SpeechRecognition.stopListening();
//     sendMessage();
//   };

//   const sendMessage = async () => {
//     try {
//       if (transcript && transcript.trim() !== '') {
//         setList(prevList => [...prevList, { prompt: transcript, bot: null }]);
        
//         const formData = new FormData();
//         formData.append('text', transcript);

//         const response = await axios.post('http://127.0.0.1:8000/api/chatbot/', formData);
//         console.log('Response from backend:', response.data);

//         // Tts.speak(response.data.reply)

//         // const utterance = new SpeechSynthesisUtterance(response.data.reply);
//         // utterance.lang = 'ko-KR'; // 음성 언어 설정
//         // window.speechSynthesis.speak(utterance);
        
//         // var url = window.URL.createObjectURL(response.data.output_audio_path);
//         // const audioResponse = new Audio();
//         // audioResponse.src = url;
//         // audioResponse.play();

//       //   if (response.status === 200) {
//       //     setTimeout(() => {
//       //         // Fetch the audio file from the server
//       //         axios.get(response.data.output_audio_path, {
//       //             responseType: 'blob' // Set response type to 'blob' to receive binary data
//       //         }).then(audioResponse => {
//       //             // Create a Blob from the received audio data
//       //             const audioBlob = new Blob([audioResponse.data], { type: 'audio/wav' });
      
//       //             // Create a URL for the Blob
//       //             const url = window.URL.createObjectURL(audioBlob);
      
//       //             // Create an Audio element and play the audio
//       //             const audioElement = new Audio(url);
//       //             audioElement.play();
//       //         }).catch(error => {
//       //             console.error('Error fetching audio file:', error);
//       //         });
//       //     }, 15000); // 15초 대기
//       // } else {
//       //     console.error('Failed to get audio file:', response.statusText);
//       // }

//       if (response.status === 200) {
//         // Set audio URL
//         setAudioUrl(response.data.output_audio_path);
//       } else {
//         console.error('Failed to get audio file:', response.statusText);
//       }

      
//         resetTranscript();
//       }
//     } catch (error) {
//       console.error('Error sending data:', error);
//     }
//   };

//   useEffect(() => {
//     // Component unmount 시 인식 중지
//     return () => {
//       SpeechRecognition.abortListening();
//     };
//   }, []);

//   useEffect(() => {
//     // 오디오 URL이 변경될 때마다 재생
//     if (audioUrl) {
//       const audioElement = new Audio(audioUrl);
//       audioElement.play();
//     }
//   }, [audioUrl]);


//   return (
//     <div>
//       {/* Show both start and stop buttons */}
//       {!isRecording ? (
//         <button onClick={startRecording}>시작</button>
//       ) : (
//         <button onClick={stopRecording}>종료</button>
//       )}
//       {/* Display transcript below the buttons */}
//       <p>입력: {transcript}</p>
//     </div>
//   );
// };

// export default Chatbot;



import React, { useState, useEffect } from 'react';
import SpeechRecognition, { useSpeechRecognition } from 'react-speech-recognition';
import axios from 'axios';

interface Props {
  isLoading: boolean;
  setIsLoading: React.Dispatch<React.SetStateAction<boolean>>;
  setList: React.Dispatch<React.SetStateAction<{ prompt: string | null; bot: any; }[]>>;
  list: { prompt: string | null; bot: any; }[];
}

const Chatbot: React.FC<Props> = ({ isLoading, setIsLoading, setList, list }) => {
  const { transcript, resetTranscript } = useSpeechRecognition();
  const [isRecording, setIsRecording] = useState<boolean>(false);
  const [audioUrl, setAudioUrl] = useState<string>('');

  const startRecording = () => {
    setIsRecording(true);
    SpeechRecognition.startListening({ language: 'ko-KR', continuous: true });
  };

  const stopRecording = () => {
    setIsRecording(false);
    SpeechRecognition.stopListening();
    sendMessage();
  };

  const sendMessage = async () => {
    try {
      if (transcript && transcript.trim() !== '') {
        setList(prevList => [...prevList, { prompt: transcript, bot: null }]);
        
        const formData = new FormData();
        formData.append('text', transcript);

        const response = await axios.post('http://127.0.0.1:8000/api/chatbot/', formData); 
        // {
        //   headers: {
        //     'Accept': 'audio/*'
        //   }
        // });
        console.log('Response from backend:', response.data);

        if (response.status === 200) {
          // Set audio URL
            setAudioUrl(response.data.output_audio_url);
        } else {
          console.error('Failed to get audio file:', response.statusText);
        }

        resetTranscript();
      }
    } catch (error) {
      console.error('Error sending data:', error);
    }
  };

  // useEffect(() => {
  //   if (audioUrl) {
  //     const audioElement = new Audio(audioUrl);
  //     audioElement.play().then(() => {
  //       // Playback started successfully
  //     }).catch((error) => {
  //       console.error('Error playing audio:', error);
  //     });
  //   }
  // }, [audioUrl]);

  useEffect(() => {
    
    if (audioUrl) {
      // Create an Audio element
      const audioElement = new Audio(audioUrl);
      audioElement.setAttribute('crossorigin', 'anonymous');

      // Wait for the audio to be fully loaded before playing
      audioElement.addEventListener('canplaythrough', () => {
        audioElement.play().then(() => {
          // Playback started successfully
        }).catch((error) => {
          console.error('Error playing audio:', error);
        });
      });

      // Handle audio loading errors
      audioElement.addEventListener('error', (error) => {
        console.error('Error loading audio:', error);
      });
    }
  }, [audioUrl]);


  return (
    <div>
      {/* Show both start and stop buttons */}
      {!isRecording ? (
        <button onClick={startRecording}>시작</button>
      ) : (
        <button onClick={stopRecording}>종료</button>
      )}
      {/* Display transcript below the buttons */}
      <p>입력: {transcript}</p>
    </div>
  );
};

export default Chatbot;
