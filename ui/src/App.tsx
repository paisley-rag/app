import { Router, Route } from "wouter";
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { Navigation } from "./components/Navigation.tsx";
import { PageKnowledgeBases } from "./components/pages/PageKnowledgeBases.tsx";
import { PageKnowledgeBase } from "./components/pages/PageKnowledgeBase.tsx";
import { PageChatbots } from "./components/pages/PageChatbots.tsx";
import { PageChatbot } from "./components/pages/PageChatbot.tsx";

const queryClient = new QueryClient();

function App() {
  return (
    <QueryClientProvider client={queryClient}>
      <Navigation />
      <main className="ml-72 p-12">
        <Router>
          <Route path="/knowledge-bases">
            <PageKnowledgeBases />
          </Route>
          <Route path="/knowledge-bases/:id">
            {(params) => <PageKnowledgeBase id={params.id} />}
          </Route>
          <Route path="/chatbots">
            <PageChatbots />
          </Route>
          <Route path="/chatbots/:id">
            {(params) => <PageChatbot id={params.id} />}
          </Route>
        </Router>
      </main>
    </QueryClientProvider>
  );
}

export default App;
