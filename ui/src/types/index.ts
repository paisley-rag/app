export interface QueryMessage {
  type: "query";
  body: string;
}

export interface ResponseMessage {
  type: "response";
  body: string;
}

export type Message = QueryMessage | ResponseMessage;
