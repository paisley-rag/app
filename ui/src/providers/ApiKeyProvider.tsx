import React from 'react';

interface ApiKeyContextType {
  apiKey: string,
  handleApiKeyChange: (key: string) => void,
}

export const ApiKeyContext = React.createContext<ApiKeyContextType>({
  apiKey: '',
  handleApiKeyChange: (_: string) => {},
});

interface ApiKeyProviderProps {
  children: React.ReactNode;
}
export const ApiKeyProvider = ({children} : ApiKeyProviderProps) => {
  const [apiKey, setApiKey] = React.useState('');

  const handleApiKeyChange = (key: string) => setApiKey(key);

  return (
    <ApiKeyContext.Provider value={ {apiKey, handleApiKeyChange } } >
      {children}
    </ApiKeyContext.Provider>
  );
};
