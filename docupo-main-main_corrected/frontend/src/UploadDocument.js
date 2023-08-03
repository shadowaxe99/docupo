import React, { useState } from 'react';
import axios from 'axios';

const UploadDocument = () => {
  const [selectedFile, setSelectedFile] = useState(null);
  const [message, setMessage] = useState('');

  const handleFileChange = (event) => {
    setSelectedFile(event.target.files[0]);
  };

  const uploadDocument = () => {
    const formData = new FormData();
    formData.append('file', selectedFile);

    axios.post('/api/upload', formData)
      .then((response) => {
        setMessage('UPLOAD_SUCCESS');
      })
      .catch((error) => {
        setMessage('UPLOAD_FAILURE');
      });
  };

  return (
    <div>
      <input type="file" id="upload-button" onChange={handleFileChange} />
      <button onClick={uploadDocument}>Upload</button>
      <p>{message}</p>
    </div>
  );
};

export default UploadDocument;
