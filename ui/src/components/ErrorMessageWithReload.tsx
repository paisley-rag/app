import { Button } from "./ui/button";
import { Typography } from "./Typography";
import { RotateCcw } from "lucide-react";

export function ErrorMessageWithReload() {
  return (
    <div className="flex flex-col items-center space-y-4">
      <Typography variant="p">
        An error occurred while fetching the data.
      </Typography>
      <Button variant="outline" onClick={() => window.location.reload()}>
        <RotateCcw className="h-5 w-5 mr-2" />
        Retry
      </Button>
    </div>
  );
}
