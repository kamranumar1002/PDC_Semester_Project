import React, { useCallback } from 'react';
import { useDropzone } from 'react-dropzone';
import { UploadCloud, FileAudio } from 'lucide-react';

const FileUploader = ({ onUpload, isUploading }) => {
  const onDrop = useCallback((acceptedFiles) => {
    if (acceptedFiles.length > 0) {
      onUpload(acceptedFiles);
    }
  }, [onUpload]);

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    accept: { 'audio/*': ['.wav', '.mp3'] }
  });

  return (
    <div 
      {...getRootProps()} 
      className={`border-2 border-dashed rounded-lg p-8 text-center cursor-pointer transition-all
        ${isDragActive ? 'border-cyan-400 bg-cyan-900/20' : 'border-gray-600 hover:border-gray-400 bg-hpc-panel'}
      `}
    >
      <input {...getInputProps()} />
      <div className="flex flex-col items-center justify-center space-y-3">
        {isUploading ? (
          <div className="animate-spin rounded-full h-10 w-10 border-b-2 border-cyan-400"></div>
        ) : (
          <>
            <UploadCloud size={48} className="text-gray-400" />
            <p className="text-lg font-medium text-gray-300">
              Drag & drop audio files here, or click to select
            </p>
            <p className="text-sm text-gray-500">Supports WAV, MP3 (Max 50MB)</p>
          </>
        )}
      </div>
    </div>
  );
};

export default FileUploader;