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
import { ProtectedRoute } from "./components/ProtectedRoute.tsx";
import { AuthProvider } from "./auth.tsx";
// import { DataTableDemo } from "./components/pages/DataTableDemo.tsx"; // testing only

const queryClient = new QueryClient();

function App() {
  return (
    <AuthProvider>
      <QueryClientProvider client={queryClient}>
        <Navigation />
        <main className="ml-60 p-6">
          <Router>
            <Switch>
              {/* <ProtectedRoute> */}
                <Route path="/knowledge-bases" component={PageKnowledgeBases} />
              {/* </ProtectedRoute>   */}
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
                <Route path="/login" component={() => <h1>Login</h1>} />
            </Switch>
          </Router>
        </main>
      </QueryClientProvider>
    </AuthProvider>
  );
}

export default App;
