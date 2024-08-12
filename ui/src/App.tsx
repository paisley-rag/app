import { Router, Route, Switch } from "wouter";
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { Navigation } from "./components/Navigation.tsx";
import { PageKnowledgeBases } from "./components/pages/PageKnowledgeBases.tsx";
import { PageKnowledgeBase } from "./components/pages/PageKnowledgeBase.tsx";
import { PageChatbots } from "./components/pages/PageChatbots.tsx";
import { PageChatbot } from "./components/pages/PageChatbot.tsx";
import { PageEvaluations } from "./components/pages/PageEvaluations.tsx";
import { PageCreateChatbot } from "./components/pages/PageCreateChatbot.tsx";
// import { DataTableDemo } from "./components/pages/DataTableDemo.tsx"; // testing only

const queryClient = new QueryClient();

function App() {
  return (
    <QueryClientProvider client={queryClient}>
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
            <Route path="/evaluations" component={PageEvaluations} />
          </Switch>
        </Router>
      </main>
    </QueryClientProvider>
  );
}

export default App;
