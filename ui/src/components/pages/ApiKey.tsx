import { Typography } from "../Typography";
// import { Button } from "@/components/ui/button";
// import { ArrowLeftIcon } from "lucide-react";
// import { useLocation } from "wouter";
import { Input } from "../ui/input";
import React from 'react';
import { ApiKeyContext } from '../../providers/ApiKeyProvider.tsx';

export function ApiKey(): React.ReactNode {
  // const [, navigate] = useLocation();
  const { apiKey, handleApiKeyChange } = React.useContext(ApiKeyContext);

  // function handleBackClick() {
  //   navigate('/');
  // }

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    handleApiKeyChange(e.target.value);
  }
  
  return (
    <>
      <header>
        <Typography variant="h4" className="mb-5 flex items-center gap-2">
          <div>API Key</div>
        </Typography>
          {/* <Typography variant="h3" className="mb-5 flex items-center gap-2">
            <Button variant="ghost" size="icon" onClick={handleBackClick}>
              <ArrowLeftIcon className="h-5 w-5" />
            </Button>
            Back
          </Typography> */}
      </header>
      <div className="grid grid-cols-2 gap-4">
        <div>
          Please enter the API key to use below:
          <Input
            type="text"
            placeholder="Enter desired API Key"
            value={apiKey}
            onChange={e => handleChange(e)}
            className="input"
          />

          <p className="mt-4 text-sm text-muted-foreground">The api key entered will be used for all HTTP requests sent by this interface.</p>
          <p className="text-sm text-muted-foreground">If you do not have a valid key, check with your network administrator.</p>
        </div>
      </div>
    </>
  )
}