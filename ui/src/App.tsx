import { Router, Route, Switch } from "wouter";
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { Navigation } from "./components/Navigation.tsx";
import { PageKnowledgeBases } from "./components/pages/PageKnowledgeBases.tsx";
import { PageKnowledgeBase } from "./components/pages/PageKnowledgeBase.tsx";
import { PageChatbots } from "./components/pages/PageChatbots.tsx";
import { PageChatbot } from "./components/pages/PageChatbot.tsx";
import { PageCreateChatbot } from "./components/pages/PageCreateChatbot.tsx";
import { PageHistory } from "./components/pages/PageHistory.tsx";
import { PageLineChart } from "./components/pages/PageLineChart.tsx";
import { ApiKey } from './components/pages/ApiKey.tsx';
import { ApiKeyProvider } from './providers/ApiKeyProvider.tsx';
// import { DataTableDemo } from "./components/pages/DataTableDemo.tsx"; // testing only

const queryClient = new QueryClient();

function App() {
  return (
    <QueryClientProvider client={queryClient}>
      <ApiKeyProvider>
      <Navigation />
      <main className="ml-60 p-6">
        <Router>
          <Switch>
            <Route path="/knowledge-bases" component={PageKnowledgeBases} />
            <Route path="/knowledge-bases/:id">
              {(params) => <PageKnowledgeBase id={params.id} />}
            </Route>
            <Route path="/chatbots" component={PageChatbots} />
            <Route path="/chatbots/create" component={PageCreateChatbot} />
            <Route path="/chatbots/:id">
              {(params) => <PageChatbot id={params.id} />}
            </Route>
            <Route path="/history" component={PageHistory} />
            <Route path="/metrics" component={PageLineChart} />
            <Route path="/api-key" component={ApiKey} />
            <Route path="/" component={ApiKey} />
          </Switch>
        </Router>
      </main>
      </ApiKeyProvider>
    </QueryClientProvider>
  );
}

export default App;
