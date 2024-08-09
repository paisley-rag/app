import { useState } from "react";
import { Message } from "../types";
import { sendQuery } from "../services/service";
import classes from './ChatContainer.module.css';

export default function ChatContainer() {
  async function handleSendMessage(e: React.SyntheticEvent) {
    e.preventDefault();
    const message: Message = { type: "query", body: messageInput };
    setMessages((prev) => [...prev, message]);
    // need to figure out how to get this to work without type assertion
    const response = (await sendQuery(messageInput)) as Message;
    setMessages((prev) => [...prev, response]);
  }

  function handleMessageInputChange(e: React.SyntheticEvent) {
    const target = e.target as HTMLInputElement;
    setMessageInput(target.value);
  }
  const [messageInput, setMessageInput] = useState("");
  const [messages, setMessages] = useState<Message[]>([
    {
      type: "response",
      body: "this is your answer based on the documents",
    },
    { type: "query", body: "i had a question about this topic" },
  ]);

  const assignClasses = (type: string) => {
    let messageClasses = [classes.message];
    let containerClasses = [classes.chat_row];
    if (type === 'query') {
      messageClasses.push(classes.query);
      containerClasses.push(classes.query_row);
    }
    if (type === 'response') {
      messageClasses.push(classes.response);
      containerClasses.push(classes.response_row);
    }
    return [
      messageClasses.join(' '),
      containerClasses.join(' ')
    ];
  }

  return (
    <div className={classes.container}>
      <div className={classes.messages_container}>
        <div className={classes.notReverse}>
          {messages.map((message: Message) => {
            const [messageClasses, containerClasses] = assignClasses(message.type);
            return (
              <div key={message.body} className={containerClasses}>
                <p className={messageClasses}>{message.body}</p>
              </div>
            );
          })}
        </div>
      </div>
      <form className={classes.chatForm} action="" onSubmit={handleSendMessage}>
        <label htmlFor="message-input" hidden></label>
        <input
          type="text"
          id="message-input"
          value={messageInput}
          onChange={handleMessageInputChange}
          className={classes.formInput}
        />
        <button type="submit">Send</button>
      </form>
    </div>
  );
}
