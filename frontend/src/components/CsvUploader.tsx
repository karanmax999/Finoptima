import React, { useRef } from 'react';
import { useFinoptimaStore } from '../store/useFinoptimaStore';
import { Upload, RefreshCw, CheckCircle, AlertTriangle } from 'lucide-react';

export const CsvUploader: React.FC = () => {
  const store = useFinoptimaStore();
  const fileInputRef = useRef<HTMLInputElement>(null);

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files[0]) {
      store.uploadCsv(e.target.files[0]);
    }
  };

  const handleDragOver = (e: React.DragEvent) => {
    e.preventDefault();
  };

  const handleDrop = (e: React.DragEvent) => {
    e.preventDefault();
    if (e.dataTransfer.files && e.dataTransfer.files[0]) {
      store.uploadCsv(e.dataTransfer.files[0]);
    }
  };

  return (
    <div className="bg-slate-900/60 backdrop-blur-md border border-slate-800/80 p-6 rounded-2xl">
      <div className="flex justify-between items-center mb-4">
        <h3 className="text-sm font-mono text-slate-400 uppercase tracking-widest flex items-center gap-2">
          <span>📂</span> Data Ingestion Layer
        </h3>
        {store.returnsData && (
          <button
            onClick={() => store.clearCache()}
            className="flex items-center gap-1 text-xs font-mono text-cyan-400 hover:text-cyan-300 transition-colors"
          >
            <RefreshCw size={12} /> Reset to Default
          </button>
        )}
      </div>

      <div
        onDragOver={handleDragOver}
        onDrop={handleDrop}
        onClick={() => fileInputRef.current?.click()}
        className="border-2 border-dashed border-slate-800 hover:border-slate-700/80 transition-all rounded-xl p-6 text-center cursor-pointer bg-slate-950/40 hover:bg-slate-950/60 group"
      >
        <input
          type="file"
          ref={fileInputRef}
          onChange={handleFileChange}
          accept=".csv"
          className="hidden"
        />
        <div className="flex flex-col items-center justify-center">
          <div className="w-10 h-10 rounded-full bg-slate-900 border border-slate-800 flex items-center justify-center text-slate-400 group-hover:text-cyan-400 transition-colors mb-2">
            <Upload size={16} />
          </div>
          <p className="text-xs text-slate-300 font-medium">
            Drag & drop custom returns/prices CSV here or <span className="text-cyan-400">browse</span>
          </p>
          <p className="text-xxs text-slate-500 font-mono mt-1">
            Format: Column Date (optional) + ticker price/returns series
          </p>
        </div>
      </div>

      {store.isUploading && (
        <div className="mt-3 flex items-center gap-2 text-xxs font-mono text-slate-400">
          <RefreshCw size={12} className="animate-spin text-cyan-400" />
          Ingesting CSV structure and computing log daily returns...
        </div>
      )}

      {store.csvUploadMessage && !store.isUploading && (
        <div className="mt-3 p-2 bg-emerald-950/30 border border-emerald-900/60 rounded flex items-start gap-2">
          <CheckCircle size={14} className="text-emerald-400 mt-0.5 shrink-0" />
          <div className="text-xxs font-mono text-emerald-400 leading-normal">
            {store.csvUploadMessage}
          </div>
        </div>
      )}

      {store.error && (
        <div className="mt-3 p-2 bg-rose-950/30 border border-rose-900/60 rounded flex items-start gap-2">
          <AlertTriangle size={14} className="text-rose-400 mt-0.5 shrink-0" />
          <div className="text-xxs font-mono text-rose-400 leading-normal">
            Error: {store.error}
          </div>
        </div>
      )}
    </div>
  );
};
export default CsvUploader;
