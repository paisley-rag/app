import { useState } from "react";
import * as service from "../services/service";
import classes from './UploadForm.module.css';

export default function UploadForm() {
  const [file, setFile] = useState<File | null>(null);

  function handleChange(e: React.FormEvent<HTMLInputElement>) {
    const target = e.target as HTMLInputElement & {
      files: FileList;
    };
    setFile(target.files[0]);
  }

  async function handleSubmit(e: React.SyntheticEvent) {
    e.preventDefault();
    if (!file) return;

    const formData = new FormData();
    formData.set("file", file);
    await service.uploadFile(formData);
  }

  return (
    <div className={classes.container}>
      <h2>Upload</h2>
      <form className={classes.uploadForm} action="" onSubmit={handleSubmit}>
        <label htmlFor="document">Document</label>
        <input
          required
          type="file"
          name="document"
          id="document"
          onChange={handleChange}
        />
        <button type="submit">Upload</button>
      </form>
    </div>
  );
}
